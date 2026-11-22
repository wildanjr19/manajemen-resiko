import ast
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import Mock

import numpy as np
import pandas as pd
from scipy.special import xlogy
from scipy.stats import chi2, norm


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'notebooks/replikasi_var_cvar_artikel_3_pembobotan.ipynb'


def load_functions(path, namespace):
    notebook = json.loads(path.read_text(encoding='utf-8'))
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        tree = ast.parse(''.join(cell['source']))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        if functions:
            exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)


class ThreeWeightingTests(unittest.TestCase):
    def setUp(self):
        self.namespace = {
            'np': np, 'pd': pd, 'norm': norm, 'chi2': chi2, 'xlogy': xlogy,
            'json': json, 'time': time, 'datetime': datetime, 'timezone': timezone,
            'LEVELS': np.array([0.95]), 'ALPHA': 0.05,
            'M': 1000, 'K': 4, 'SEED': 2024, 'WINDOW': 120, 'RESUME_ROLLING': True,
            'TICKERS': ['BBCA.JK', 'BMRI.JK', 'BBRI.JK'],
            'MANUAL_WEIGHTS': {'BBCA.JK': 0.5, 'BMRI.JK': 0.3, 'BBRI.JK': 0.2},
        }
        load_functions(NOTEBOOK, self.namespace)
        rng = np.random.default_rng(17)
        self.frame = pd.DataFrame(
            rng.normal(size=(123, 3)) @ np.array([[0.02, 0.004, 0.002],
                                                               [0, 0.01, 0.003], [0, 0, 0.015]]),
            index=pd.bdate_range('2024-01-01', periods=123), columns=self.namespace['TICKERS'])

    def test_gmv_matches_independent_formula_and_original_monte_carlo(self):
        fit = self.namespace['fit_portfolio'](self.frame, 'GMV')
        inverse = np.linalg.inv(self.frame.cov().to_numpy())
        expected = inverse @ np.ones(3) / np.sum(inverse)
        np.testing.assert_allclose(fit['weights'], expected, rtol=1e-12)
        for weights in [np.ones(3) / 3, np.array([0.5, 0.3, 0.2])]:
            self.assertLessEqual(fit['sigma_p'] ** 2, weights @ self.frame.cov().to_numpy() @ weights + 1e-15)
        old = dict(self.namespace)
        load_functions(ROOT / 'notebooks/replikasi_var_cvar_artikel.ipynb', old)
        baseline = old['fit_gmv'](self.frame)
        actual = self.namespace['run_mc'](fit, 1000, 4, self.namespace['make_seed'](2))
        expected_mc = old['run_mc'](baseline, 1000, 4, old['make_seed'](2))
        for observed, reference in zip(actual, expected_mc):
            pd.testing.assert_frame_equal(observed, reference)

    def test_fixed_weights_follow_ticker_order_and_normal_projection(self):
        fit = self.namespace['fit_portfolio']
        for scheme, weights in [('Sama rata', np.ones(3) / 3), ('Manual 50/30/20', np.array([0.5, 0.3, 0.2]))]:
            model = fit(self.frame, scheme)
            np.testing.assert_allclose(model['weights'], weights)
            self.assertAlmostEqual(model['mu_p'], (self.frame @ weights).mean())
            self.assertAlmostEqual(model['sigma_p'], (self.frame @ weights).std(ddof=1))
        reordered = fit(self.frame.iloc[:, ::-1], 'Manual 50/30/20')
        np.testing.assert_array_equal(reordered['weights'], [0.2, 0.3, 0.5])

    def test_bad_manual_weights_fail_without_normalization(self):
        self.namespace['MANUAL_WEIGHTS']['BBCA.JK'] = 0.7
        with self.assertRaises(ValueError):
            self.namespace['fit_portfolio'](self.frame, 'Manual 50/30/20')
        with self.assertRaises(ValueError):
            self.namespace['fit_portfolio'](self.frame, 'unknown')

    def test_fractional_cvar_tail_and_normal_analytic_reference(self):
        risk = self.namespace['risk_from_losses'](np.arange(10), np.array([0.75])).iloc[0]
        self.assertAlmostEqual(risk['var'], 6.75)
        self.assertAlmostEqual(risk['cvar'], (9 + 8 + 0.5 * 7) / 2.5)
        reference = self.namespace['normal_risk']({'mu_p': 0.001, 'sigma_p': 0.02}, np.array([0.95])).iloc[0]
        self.assertAlmostEqual(reference['var_normal'], 0.03189707253902944)
        self.assertAlmostEqual(reference['cvar_normal'], 0.04025425615014851)

    def test_predictions_use_training_only_and_scheme_specific_realized_loss(self):
        train, realized, date = self.frame.iloc[:120], self.frame.iloc[120], self.frame.index[120]
        for scheme in ['GMV', 'Sama rata', 'Manual 50/30/20']:
            prediction = self.namespace['predict_one_day'](train, realized, date, scheme)
            changed = self.namespace['predict_one_day'](train, realized * 5, date, scheme)
            weights = np.array(prediction['parameters']['weights'])
            self.assertEqual(len(prediction['predictions']), 3)
            for row, altered in zip(prediction['predictions'], changed['predictions']):
                self.assertEqual(row['var'], altered['var'])
                self.assertAlmostEqual(row['loss'], -realized.to_numpy() @ weights)
                self.assertEqual(row['breach'], int(row['loss'] > row['var']))
                self.assertLess(pd.Timestamp(row['train_end']), date)
                self.assertEqual(row['skema'], scheme)

    def test_checkpoint_resume_and_scheme_mismatch(self):
        rolling = self.namespace['rolling_backtest']
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            first = rolling(self.frame.iloc[:122], folder, 'fixture', 'Sama rata')
            self.namespace['predict_one_day'] = Mock(side_effect=AssertionError('Checkpoint harus dipakai.'))
            resumed = rolling(self.frame.iloc[:122], folder, 'fixture', 'Sama rata')
            for actual, expected in zip(resumed, first):
                pd.testing.assert_frame_equal(actual, expected)
            with self.assertRaises(ValueError):
                rolling(self.frame.iloc[:122], folder, 'fixture', 'GMV')


if __name__ == '__main__':
    unittest.main()
