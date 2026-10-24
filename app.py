from pathlib import Path
import pandas as pd
import streamlit as st
from core import prioritise, experiment

ROOT=Path(__file__).parent
st.set_page_config(page_title='MigrationLead AI',page_icon='📊',layout='wide')
st.title('MigrationLead AI')
st.caption('An independent portfolio concept by Navya Ravindran • Prepared for discussion with Immatrix')
st.warning('Synthetic demonstration. No company affiliation, actual client results or visa-approval predictions.')
a,b,c=st.tabs(['Daily follow-up queue','Experimental ML lab','Business case'])
with a:
    st.subheader('Start with Excel. Give every enquiry a next step.')
    st.write('Scores below are transparent business rules, not conversion probabilities. Use a 48-hour snapshot of each enquiry. All leads still receive a minimum follow-up service.')
    upload=st.file_uploader('Optional anonymised CSV export from Excel',type=['csv'])
    st.caption('Local demonstration only: do not upload customer data to a public/shared deployment. CSV schema: see docs/DATA_DICTIONARY.md.')
    try:
        raw=pd.read_csv(upload) if upload else pd.read_csv(ROOT/'data/sample_leads.csv')
        ranked=prioritise(raw)
        x,y,z=st.columns(3)
        x.metric('Leads in snapshot',len(ranked)); y.metric('High priority',int((ranked.priority=='High').sum())); z.metric('Slow initial responses',int((ranked.response_hours>12).sum()))
        chosen=st.multiselect('Priority filter',['High','Medium','Standard'],default=['High','Medium','Standard'])
        view=ranked[ranked.priority.isin(chosen)]
        st.dataframe(view[['lead_id','source','service','rule_score','priority','reason','next_action']],hide_index=True,width='stretch')
        # Export only controlled fields; never reflect arbitrary uploaded spreadsheet formulas.
        export=view[['lead_id','rule_score','priority','next_action']].copy()
        export['lead_id']=export.lead_id.astype(str).map(lambda s: "'"+s if s.lstrip().startswith(('=','+','-','@','\t','\r')) else s)
        st.download_button('Download follow-up queue for Excel',export.to_csv(index=False),'follow_up_queue.csv','text/csv')
        st.bar_chart(ranked.groupby('source',observed=True).size().rename('Enquiries'))
        with st.expander('How the rule score works'):
            st.write('40 points: consultation booked; 30: at least 3 interactions; 20: engagement in the last 12 hours; 10: initial response took more than 12 hours, signalling a recovery action. High ≥60; Medium 30–59; Standard <30. Provisional rules require manager agreement.')
    except (ValueError,TypeError,KeyError,pd.errors.ParserError) as exc:
        st.error(f'Please correct the CSV: {exc}')
with b:
    st.subheader('Future capability: learned conversion ranking')
    st.write('This model learns only from simulated history. It is not applied to uploaded business data. The simulated outcomes reflect assumptions in the generator.')
    @st.cache_data
    def evaluate():
        _,report,pred=experiment(pd.read_csv(ROOT/'data/synthetic_history.csv'))
        return report,pred
    report,pred=evaluate()
    st.json(report)
    st.write('Precision at 20%: proportion of the top-ranked fifth who converted. Capture: fraction of all conversions in that group. Neither proves a causal improvement.')
    st.dataframe(pred[['lead_id','demo_probability','converted_30d']].sort_values('demo_probability',ascending=False).head(20),hide_index=True)
with c:
    st.subheader('A low-resource pilot, without replacing Excel')
    st.markdown((ROOT/'docs/CLIENT_PROPOSAL.md').read_text())
