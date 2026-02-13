
from jinja2 import Template, StrictUndefined

# Simulate key missing
anom_data_missing = {
    'hash': '0x123',
    # 'amount' is missing
    'anomaly_score': 0.85,
    'reasons': ['test'],
    'is_suspicious': True
}

anomalies = [anom_data_missing]

template_str = """
{% for anom in anomalies %}
    Amount: {{ "%.4f"|format(anom['amount']) }}
{% endfor %}
"""

print("--- Testing missing key with format ---")
try:
    t = Template(template_str)
    print(t.render(anomalies=anomalies))
    print("SUCCESS: Rendered with missing key (Undefined).")
except Exception as e:
    print(f"FAIL: {e}")

# What if 'amount' is None?
anom_data_none = {
    'hash': '0x123',
    'amount': None,
    'anomaly_score': 0.85,
    'reasons': [],
    'is_suspicious': False
}
anomalies_none = [anom_data_none]

print("\n--- Testing None value ---")
try:
    t = Template(template_str)
    print(t.render(anomalies=anomalies_none))
    print("SUCCESS: Rendered with None.")
except Exception as e:
    print(f"FAIL: {e}")
