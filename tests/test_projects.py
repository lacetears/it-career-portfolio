import importlib.util,json,sqlite3
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
security=module('security','cybersecurity/detect.py')
analytics=module('analytics','data-analytics/analyze.py')
helpdesk=module('helpdesk_app','helpdesk/app.py')
def events(): return [json.loads(r) for r in (ROOT/'cybersecurity/data/auth_events.jsonl').read_text().splitlines()]
def test_attack_and_benign():
    alerts=security.detect(events());assert [a['rule'] for a in alerts]==['repeated_login_failure','success_after_failures'];assert all(a['host']=='lab-linux' for a in alerts)
def test_out_of_order(): assert security.detect(events()[::-1])==security.detect(events())
def test_window_expiry():
    rows=events()[:5];rows[-1]['timestamp']='2026-01-15T09:20:00Z';assert security.detect(rows)==[]
def test_separate_hosts():
    rows=events()[:5];rows[-1]['host']='other';assert security.detect(rows)==[]
def test_timezone_required():
    rows=events()[:1];rows[0]['timestamp']='2026-01-15T09:00:00'
    with pytest.raises(ValueError):security.detect(rows)
def valid_row(): return dict(order_id='A',order_date='2025-01-01',region=' north ',product='Laptop',quantity='2',unit_price_cents='10001',unit_cost_cents='5000',discount_pct='5',status='Completed')
def test_cleaning_rounding_dedup():
    row=valid_row(); good,rejected,dupes=analytics.clean([row,row,dict(row,order_id='B',quantity='-1')]);assert len(good)==1;assert dupes==1;assert len(rejected)==1;assert good[0]['region']=='North';assert good[0]['net_revenue_cents']==19002;assert good[0]['gross_profit_cents']==9002
def test_returns_no_revenue():
    rows,_,_=analytics.clean([dict(valid_row(),status='Returned')]);assert rows[0]['net_revenue_cents']==0;assert rows[0]['gross_profit_cents']==0
def test_bad_date():
    good,rejected,_=analytics.clean([dict(valid_row(),order_date='2025-02-30')]);assert not good;assert len(rejected)==1
@pytest.fixture
def client(tmp_path):
    app=helpdesk.create_app({'TESTING':True,'SECRET_KEY':'test-only','DATABASE':str(tmp_path/'test.db')});return app.test_client()
def csrf(client):
    client.get('/')
    with client.session_transaction() as session:return session['csrf']
def submit(client,**kwargs):
    data=dict(title='Printer offline',description='Needs investigation',requester='Demo',priority='High',csrf=csrf(client));data.update(kwargs);return client.post('/tickets',data=data)
def test_ticket_lifecycle(client):
    assert submit(client).status_code==302
    response=client.post('/tickets/1',data=dict(csrf=csrf(client),status='Resolved',priority='Low',assignee='Alex'),follow_redirects=True)
    assert response.status_code==200;assert b'Alex' in response.data;assert b'Ticket created' in response.data
    assert b'Printer offline' in client.get('/?q=Printer&status=Resolved').data
    assert b'Printer offline' not in client.get('/?status=Open').data
def test_csrf(client): assert client.post('/tickets',data={'title':'x'}).status_code==400
def test_invalid_priority(client):assert submit(client,priority='Unknown').status_code==400
def test_xss_escaped(client):
    submit(client,title='<script>alert(1)</script>');response=client.get('/tickets/1');assert b'<script>alert(1)</script>' not in response.data;assert b'&lt;script&gt;' in response.data
def test_sql_injection_search(client):
    submit(client);assert client.get("/?q=' OR 1=1 --").status_code==200;assert client.get('/tickets/1').status_code==200
def test_missing_ticket(client):assert client.get('/tickets/999').status_code==404
def test_pipeline_totals():
    import csv
    rows=list(csv.DictReader((ROOT/'data-analytics/output/clean_sales.csv').open()))
    quality=json.loads((ROOT/'data-analytics/output/quality_report.json').read_text())
    assert quality['input_rows']==quality['valid_rows']+quality['duplicate_rows']+quality['rejected_rows']
    assert len(rows)==1200;assert quality['rejected_rows']==3;assert quality['duplicate_rows']==10
    result=json.loads((ROOT/'data-analytics/output/query_results.json').read_text())
    assert round(sum(r['revenue_usd'] for r in result['monthly'])*100)==sum(int(r['net_revenue_cents']) for r in rows)
