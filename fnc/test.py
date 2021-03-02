import sys, os.path as path
from builtins import isinstance
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from pipeline import single_data_run,load_model,generate_features_single_test
import time

from fnc.refs.utils.dataset import DataSet
from fnc.refs.utils.testDataset  import TestDataSet
import csv



class Predict():
    def __init__(self):
        self.data_path = "%s/data/fnc-1" % (path.dirname(path.dirname(path.abspath(__file__))))
        self.splits_dir = "%s/data/fnc-1/splits" % (path.dirname(path.dirname(path.abspath(__file__))))
        self.features_dir="%s/data/fnc-1/features" % (path.dirname(path.dirname(path.abspath(__file__))))
        self.result_file_folder = "%s" % (path.dirname(path.dirname(path.abspath(__file__))))
        self.embeddPath = "%s/data/embeddings/google_news/GoogleNews-vectors-negative300.bin.gz" % (path.dirname(path.dirname(path.abspath(__file__))))
       
        self.Xs = dict()
        self.ys = dict()

        # (scorer_type, [normal features], [non-bleeding features])
        self.feature_list = [
            # ORIGINAL FEATURES OF FNC-1 BEST SUBMISSION 3)
            ('voting_mlps_hard',
             ['overlap',
              'refuting',
              'polarity',
              'hand',
              #'NMF_fit_all_incl_holdout_and_test',
              #'latent_dirichlet_allocation_incl_holdout_and_test',
              #'latent_semantic_indexing_gensim_holdout_and_test',
              #'NMF_fit_all_concat_300_and_test',
              #'word_ngrams_concat_tf5000_l2_w_holdout_and_test',
              'stanford_wordsim_1sent'],
             [])
        ]

        # define and create parent folder to save all trained classifiers into
        self.parent_folder = "%s/data/fnc-1/mlp_models/" % (path.dirname(path.dirname(path.abspath(__file__))))
        # self.fnc_result_folder = "%s/data/fnc-1/fnc_results/" % (path.dirname(path.dirname(path.abspath(__file__))))


        scorer_type = 'voting_mlps_hard'
        # load model [scorer_type]_final_2 classifier
        self.filename = scorer_type + "_final.sav"
        self.load_clf = load_model(self.parent_folder + scorer_type + "_final_new_2/",self.filename)  # TODO set the correct path to the classifier here
        


        print("Load model for final prediction of test set: " + self.parent_folder + scorer_type + "_final_new_2/" + self.filename)

        


    def single_data(self,a_headline, a_body):
        d = DataSet('', a_headline, a_body)

        for scorer_type, features, non_bleeding_features in self.feature_list:
            d = TestDataSet('', a_headline, a_body)

            # generate features for the unlabeled testing set
            X_final_test = generate_features_single_test(d.stances, d, str("final_test"), features, self.features_dir)
        
            # predict classes and turn into labels
            y_predicted = self.load_clf.predict_proba(X_final_test)
            labeled_prediction = dict(zip(["agree", "disagree", "discuss", "unrelated"],
                                    ['{:.2f}'.format(s_c) for s_c in y_predicted[0]]))
            #predicted = [LABELS[int(a)] for a in y_predicted]
            #print("Prediction Length: ", len(predicted))
            print("Prediction Raw: ", labeled_prediction)
            #print("Predicted output: ", predicted)
            return labeled_prediction


title= 'Here when the US will see a lot more vaccine doses'
body = 'A fourth Covid-19 vaccine could become available in the US in April, when AstraZeneca could secure FDA authorization of its vaccine. Dr. Ruud Dobber, the executive vice president and president of AstraZeneca biopharmaceuticals business unit, said the company will immediately release 30 million doses upon authorization of the vaccine and up to 50 million doses by the end of April.'

# load the model and call the class when you recive request
start_time = time.time()
single_data_run(title,body)
original = time.time()-start_time


# load the model when starting the server
pr = Predict()

# recive a request and call the class
start_time = time.time()
pr.single_data(title,body)
modefied = time.time()-start_time







print('----------------------')
print('priv time',original)
print('new data',modefied)
