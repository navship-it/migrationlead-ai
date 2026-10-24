"""Explainable operational rules and reproducible synthetic ML experiment."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss

FEATURES = ['source','service','response_hours','consultation_booked','interactions_48h','recency_hours']
NUMERIC = FEATURES[2:]

def validate(df):
    required = ['lead_id', 'enquiry_date'] + FEATURES
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    df = df.copy()
    if df.empty or df['lead_id'].isna().any() or df['lead_id'].duplicated().any():
        raise ValueError('Provide nonempty data with unique, nonblank lead IDs.')
    df['enquiry_date'] = pd.to_datetime(df['enquiry_date'], errors='raise')
    for col in ['source','service']:
        if df[col].isna().any() or df[col].astype(str).str.strip().eq('').any():
            raise ValueError(f'{col} must not be blank.')
    bounds = {'response_hours':(0,48),'consultation_booked':(0,1),'interactions_48h':(0,100),'recency_hours':(0,48)}
    for col,(lo,hi) in bounds.items():
        df[col] = pd.to_numeric(df[col], errors='raise')
        if not np.isfinite(df[col]).all() or not df[col].between(lo,hi).all():
            raise ValueError(f'{col} must be between {lo} and {hi}.')
    if not df['consultation_booked'].isin([0,1]).all() or not (df['interactions_48h'] % 1 == 0).all():
        raise ValueError('Consultation must be 0/1 and interactions must be whole numbers.')
    return df

def prioritise(df):
    """Business-rule score, NOT a probability or learned model."""
    out = validate(df)
    out['rule_score'] = (40*out.consultation_booked + 30*(out.interactions_48h>=3) + 20*(out.recency_hours<=12) + 10*(out.response_hours>12)).astype(int)
    out['priority'] = pd.cut(out.rule_score, [-1,29,59,100], labels=['Standard','Medium','High'])
    out['reason'] = out.apply(lambda r: '; '.join(filter(None,[
        'Consultation booked' if r.consultation_booked else '',
        'Three or more interactions' if r.interactions_48h>=3 else '',
        'Recent engagement' if r.recency_hours<=12 else '',
        'Slow initial response: recovery follow-up' if r.response_hours>12 else ''
    ])) or 'Standard follow-up',axis=1)
    out['next_action'] = np.where(out.consultation_booked==1,'Confirm consultation and next steps','Consultant to review and follow up')
    return out.sort_values(['rule_score','enquiry_date'],ascending=[False,True])

def generate(n=5000, seed=42):
    rng=np.random.default_rng(seed)
    dates=pd.Timestamp('2025-01-01')+pd.to_timedelta(rng.integers(0,365,n),unit='D')
    df=pd.DataFrame({'lead_id':[f'DEMO-{i:05}' for i in range(n)],'enquiry_date':dates,
        'source':rng.choice(['Website','WhatsApp','Referral','Social media'],n),
        'service':rng.choice(['Study','Work permit','Tourist','Skilled migration'],n),
        'response_hours':np.round(rng.uniform(0,48,n),1),
        'consultation_booked':rng.binomial(1,.3,n),
        'interactions_48h':rng.poisson(2,n),
        'recency_hours':np.round(rng.uniform(0,48,n),1)})
    # Deliberately simulated relationships plus unobserved variation; not company evidence.
    z=-2.3+1.2*df.consultation_booked+.24*df.interactions_48h-.025*df.response_hours-.012*df.recency_hours+.5*(df.source=='Referral')+rng.normal(0,1,n)
    df['converted_30d']=rng.binomial(1,1/(1+np.exp(-z)))
    return df.sort_values('enquiry_date').reset_index(drop=True)

def experiment(df):
    df=validate(df)
    if 'converted_30d' not in df or not df.converted_30d.isin([0,1]).all():
        raise ValueError('Binary converted_30d outcomes are required.')
    # 30-day outcome window plus 2-day scoring window must mature before test begins.
    cutoff=pd.Timestamp('2025-10-01')
    train=df[df.enquiry_date+pd.Timedelta(days=32)<cutoff]
    test=df[df.enquiry_date>=cutoff].copy()
    if train.converted_30d.nunique()<2 or test.converted_30d.nunique()<2:
        raise ValueError('Both splits need converted and unconverted leads.')
    pre=ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore'),['source','service']),('num',StandardScaler(),NUMERIC)])
    model=make_pipeline(pre,LogisticRegression(max_iter=1000,random_state=42))
    model.fit(train[FEATURES],train.converted_30d)
    p=model.predict_proba(test[FEATURES])[:,1]
    test['demo_probability']=p
    k=max(1,int(np.ceil(len(test)*.2)))
    y=test.converted_30d.to_numpy()
    def metrics(scores):
        idx=np.argsort(-np.asarray(scores),kind='stable')[:k]
        return {'precision_at_20pct':float(y[idx].mean()),'conversion_capture_at_20pct':float(y[idx].sum()/y.sum())}
    rule=prioritise(test).set_index('lead_id').loc[test.lead_id,'rule_score'].to_numpy()
    report={'disclosure':'Synthetic simulation only. No demonstrated client impact. Outcomes assumed complete by 2026-02-02.',
        'train_rows':len(train),'test_rows':len(test),'test_conversion_rate':float(y.mean()),
        'ml':{**metrics(p),'average_precision':float(average_precision_score(y,p)),'brier_score':float(brier_score_loss(y,p))},
        'rules':metrics(rule),'newest_first':metrics(test.enquiry_date.astype('int64'))}
    return model,report,test

if __name__=='__main__':
    import json
    Path('data').mkdir(exist_ok=True); Path('reports').mkdir(exist_ok=True)
    df=generate(); df.to_csv('data/synthetic_history.csv',index=False)
    df.tail(100).drop(columns='converted_30d').to_csv('data/sample_leads.csv',index=False)
    _,report,predictions=experiment(df)
    predictions.to_csv('reports/synthetic_test_predictions.csv',index=False)
    Path('reports/model_metrics.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
