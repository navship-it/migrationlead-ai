import unittest
import numpy as np
from core import generate, prioritise, validate, experiment, FEATURES
class TestCore(unittest.TestCase):
    def test_reproducible_and_schema(self):
        self.assertTrue(generate().equals(generate()))
        df=generate(30); self.assertEqual(len(validate(df)),30)
        self.assertNotIn('converted_30d',FEATURES)
    def test_rules(self):
        df=generate(2)
        df.loc[:,['consultation_booked','interactions_48h','recency_hours','response_hours']]=[1,3,2,20]
        self.assertTrue((prioritise(df).rule_score==100).all())
    def test_reject_bad_data(self):
        df=generate(10); df.loc[0,'response_hours']=np.nan
        with self.assertRaises(ValueError): validate(df)
        df=generate(10); df.loc[1,'lead_id']=df.loc[0,'lead_id']
        with self.assertRaises(ValueError): validate(df)
    def test_temporal_holdout(self):
        _,r,p=experiment(generate())
        self.assertGreater(r['train_rows'],100)
        self.assertTrue((p.enquiry_date>='2025-10-01').all())
        self.assertTrue(p.demo_probability.between(0,1).all())
if __name__=='__main__': unittest.main()
