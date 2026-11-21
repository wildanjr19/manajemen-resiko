import ast
from contextlib import redirect_stdout
from datetime import datetime, timezone
import hashlib
import inspect
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]


class NotebookDownloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads((ROOT / 'notebooks' / 'replikasi_var_cvar.ipynb').read_text(encoding='utf-8'))
        cls.source = next(
            ''.join(cell['source']) for cell in notebook['cells']
            if cell['cell_type'] == 'code' and ''.join(cell['source']).startswith('request_spec =')
        )
        cls.download_signature = inspect.signature(yf.download)

    def configuration(self):
        return {
            'TICKERS': ['BBCA.JK', 'BMRI.JK', 'BBRI.JK'],
            'DOWNLOAD_START': '2023-12-01', 'DOWNLOAD_END': '2024-12-31',
            'RETURN_START': '2024-01-02', 'RETURN_END': '2024-12-30',
        }

    def test_request_matches_yfinance_api_and_explicit_dates(self):
        namespace = self.configuration()
        assignment = ast.parse(self.source).body[0]
        exec(compile(ast.Module(body=[assignment], type_ignores=[]), '<request_spec>', 'exec'), namespace)
        arguments = self.download_signature.bind(
            **namespace['request_spec'], threads=False, progress=False, timeout=30
        ).arguments
        self.assertEqual(arguments['start'], namespace['DOWNLOAD_START'])
        self.assertEqual(arguments['end'], namespace['DOWNLOAD_END'])
        self.assertIs(arguments['auto_adjust'], False)

    def test_download_and_cache_preserve_prices_without_second_request(self):
        with tempfile.TemporaryDirectory(prefix='download-test-') as task_directory:
            directory = Path(task_directory).resolve()
            self.assertEqual(directory.parent, Path(tempfile.gettempdir()).resolve())
            namespace = self.configuration()
            dates = pd.to_datetime(['2023-12-29', '2024-01-02', '2024-01-03'])
            adjusted = pd.DataFrame(
                [[9000, 6000, 5000], [9100, 6050, 5025], [9050, 6100, 5100]],
                index=dates, columns=namespace['TICKERS'], dtype=float,
            )
            fixture = pd.concat({'Adj Close': adjusted, 'Close': adjusted * 1.02}, axis=1)

            def strict_download(*args, **kwargs):
                self.download_signature.bind(*args, **kwargs)
                return fixture.copy()

            download = Mock(side_effect=strict_download)
            namespace.update({
                'RAW_DIR': directory, 'TABLE_DIR': directory, 'PROCESSED_DIR': directory,
                'REFRESH_DATA': False, 'ALLOW_MISSING_INTERVALS': False,
                'VERSIONS': {'yfinance': yf.__version__}, 'yf': SimpleNamespace(download=download),
                'pd': pd, 'np': np, 'json': json, 'hashlib': hashlib,
                'datetime': datetime, 'timezone': timezone, 'display': lambda value: None,
            })
            with redirect_stdout(io.StringIO()):
                exec(compile(self.source, '<notebook_download>', 'exec'), namespace)
            download.assert_called_once()
            pd.testing.assert_frame_equal(namespace['prices'], adjusted)
            metadata = json.loads((directory / 'yahoo_metadata.json').read_text(encoding='utf-8'))
            self.assertEqual(metadata['request']['end'], '2024-12-31')
            self.assertEqual(metadata['sha256_csv'], hashlib.sha256((directory / 'yahoo_ohlcv.csv').read_bytes()).hexdigest())

            download.reset_mock(side_effect=True)
            download.side_effect = AssertionError('Cache harus dipakai tanpa mengunduh ulang.')
            with redirect_stdout(io.StringIO()):
                exec(compile(self.source, '<notebook_download_cached>', 'exec'), namespace)
            download.assert_not_called()
            pd.testing.assert_frame_equal(namespace['prices'], adjusted)


if __name__ == '__main__':
    unittest.main()
