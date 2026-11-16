"""Diagnosis tambahan pada return yang dipakai run notebook utama, tanpa filtering."""

from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform

import numpy as np
import pandas as pd
from scipy.stats import anderson, normaltest, shapiro


def main():
    output_dir = Path(__file__).resolve().parent
    root = output_dir.parent
    config_path = root / 'hasil_tanpa_filter' / 'konfigurasi_eksekusi.json'
    returns_path = root / 'data' / 'processed' / 'return_mentah.csv'
    prices_path = root / 'data' / 'processed' / 'harga_adjusted.csv'
    config = json.loads(config_path.read_text(encoding='utf-8'))
    returns = pd.read_csv(returns_path, index_col=0, parse_dates=True, float_precision='round_trip')
    prices = pd.read_csv(prices_path, index_col=0, parse_dates=True, float_precision='round_trip')
    alpha = float(config['alpha'])

    if config['perlakuan'] != 'tanpa_filter' or config['n_removed_full'] != 0:
        raise ValueError('Konfigurasi run utama harus memakai seluruh return tanpa filtering.')
    if returns.columns.tolist() != config['tickers'] or len(returns) != config['n_returns']:
        raise ValueError('Saham atau jumlah return berbeda dari run notebook utama.')
    if returns.index.has_duplicates or not returns.index.is_monotonic_increasing:
        raise ValueError('Tanggal return harus unik dan berurutan.')
    if len(returns) < 20 or not np.isfinite(returns.to_numpy()).all():
        raise ValueError('Diagnosis memerlukan minimal 20 return finite tanpa nilai hilang.')
    if (returns.std(ddof=1) <= 0).any():
        raise ValueError('Return konstan tidak dapat dipakai untuk diagnosis normalitas.')
    if not 0 < alpha < 1:
        raise ValueError('Taraf signifikansi harus berada di antara 0 dan 1.')

    reconstructed = np.log(prices / prices.shift(1)).loc[
        config['return_start']:config['return_end']]
    if not returns.index.equals(reconstructed.index) or not returns.columns.equals(reconstructed.columns):
        raise ValueError('Tanggal atau saham return tidak cocok dengan harga pada periode notebook.')
    np.testing.assert_allclose(returns.to_numpy(), reconstructed.to_numpy(), rtol=0, atol=1e-15)

    rows = []
    for ticker in config['tickers']:
        values = returns[ticker].to_numpy(dtype=float)
        for name, test in [('Shapiro-Wilk', shapiro), ("D'Agostino-Pearson", normaltest)]:
            result = test(values, nan_policy='raise')
            statistic, p_value = float(result.statistic), float(result.pvalue)
            if not np.isfinite([statistic, p_value]).all() or not 0 <= p_value <= 1:
                raise ArithmeticError(f'Hasil {name} tidak valid untuk {ticker}.')
            rows.append({
                'ticker': ticker, 'n': len(values), 'uji': name, 'statistik': statistic,
                'p_value': p_value, 'nilai_kritis': None, 'alpha': alpha,
                'keputusan': 'Tolak H0' if p_value < alpha else 'Tidak menolak H0',
            })

        result = anderson(values, dist='norm')
        positions = np.flatnonzero(np.isclose(result.significance_level, 100 * alpha))
        if len(positions) != 1:
            raise ValueError(f'Tabel Anderson-Darling tidak menyediakan taraf {alpha:.2%}.')
        statistic = float(result.statistic)
        critical = float(result.critical_values[positions[0]])
        if not np.isfinite([statistic, critical]).all():
            raise ArithmeticError(f'Hasil Anderson-Darling tidak valid untuk {ticker}.')
        rows.append({
            'ticker': ticker, 'n': len(values), 'uji': 'Anderson-Darling',
            'statistik': statistic, 'p_value': None, 'nilai_kritis': critical, 'alpha': alpha,
            'keputusan': 'Tolak H0' if statistic > critical else 'Tidak menolak H0',
        })

    results = pd.DataFrame(rows)
    results.to_csv(output_dir / 'hasil_uji.csv', index=False, float_format='%.17g')
    metadata = {
        'tujuan': 'Diagnosis eksploratif tambahan; tidak mengubah metode notebook utama',
        'perlakuan': 'tanpa_filter', 'tickers': config['tickers'],
        'return_start': config['return_start'], 'return_end': config['return_end'],
        'tanggal_return_pertama': str(returns.index.min().date()),
        'tanggal_return_terakhir': str(returns.index.max().date()),
        'n_returns': len(returns), 'n_removed': 0, 'alpha': alpha,
        'uji': ['Shapiro-Wilk', "D'Agostino-Pearson", 'Anderson-Darling'],
        'aturan_p_value': 'Tolak H0 jika p_value < alpha',
        'aturan_anderson_darling': 'Tolak H0 jika statistik > nilai_kritis pada taraf alpha',
        'catatan_p_value_ad': 'Tidak tersedia pada scipy.stats.anderson versi terpasang; CSV dikosongkan',
        'sha256_input': {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [config_path, returns_path, prices_path]
        },
        'sha256_script': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'versions': {name: version(name) for name in ['numpy', 'pandas', 'scipy']},
        'python': platform.python_version(),
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    }
    (output_dir / 'konfigurasi_uji.json').write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
    print(f"Periode: {config['return_start']} s.d. {config['return_end']} | n={len(returns)} | alpha={alpha}")
    print(results.to_string(index=False, float_format=lambda value: f'{value:.6g}', na_rep='-'))
    print('Hasil tersimpan di:', output_dir)


if __name__ == '__main__':
    main()
