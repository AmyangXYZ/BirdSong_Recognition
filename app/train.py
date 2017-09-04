#coding=utf-8
from HMM import *
from tqdm import tqdm
from sigproc import SigProc
from sklearn.externals import joblib

def train_wavs(data_folder):
    hmm_models = []
    test_set = []
    for dirname in os.listdir(data_folder):
        # Get the name of the subfolder
        subfolder = os.path.join(data_folder, dirname)
        if not os.path.isdir(subfolder):
            continue
        # Extract the label
        label = subfolder[subfolder.rfind('/') + 1:]
        print '[*] '+label
        # Initialize variables
        X = np.array([])
        y_words = []

        # Iterate through the audio files (leaving 1 file for testing in each class)
        files = [x for x in os.listdir(subfolder) if x.endswith('.wav')]
        train_set = files[:-2]
        test_set.append([os.path.join(subfolder,i) for i in files[-2:]])
        for filename in tqdm(train_set):
            # Extract Feature
            print 
            filepath = os.path.join(subfolder,filename)
            try:
                mfcc_features = SigProc(filepath).MFCC().T
            except:
                pass
            # Append to the variable X
            if len(X) == 0:
                X = mfcc_features
            else:
                X = np.append(X, mfcc_features, axis=0)

            # Append the label
            y_words.append(label)

        # Train and save HMM model
        hmm_trainer = HMMTrainer()
        hmm_trainer.train(X)
        hmm_models.append((hmm_trainer, label))
        joblib.dump(hmm_trainer, subfolder + "/ModelTrained.pkl")
        hmm_trainer = None
    return test_set

def recognize(mfcc_features):
    # Load Models
    hmm_models = []

    data_folder = '/home/amyang/Speech-Recognition/BirdSongData/data'
    for dirname in os.listdir(data_folder):
        # Get the name of the subfolder
        subfolder = os.path.join(data_folder, dirname)
        if not os.path.isdir(subfolder):
            continue
        # Extract the label
        label = subfolder[subfolder.rfind('/') + 1:]
        hmm_model = joblib.load(subfolder + "/ModelTrained.pkl")
        hmm_models.append((hmm_model, label))


    # Define variables
    max_score = None
    output_label = None
    # Iterate through all HMM models and pick
    # the one with the highest score
    for item in hmm_models:
        hmm_model, label = item
        score = hmm_model.get_score(mfcc_features.T)
        if score > max_score:
            max_score = score
            output_label = label
    return output_label

if __name__ == "__main__":
    data_folder = '/home/amyang/Speech-Recognition/BirdSongData/data'

#    test_set = train_wavs(data_folder)
    for dirname in os.listdir(data_folder):
        # Get the name of the subfolder
        subfolder = os.path.join(data_folder, dirname)

        label = subfolder[subfolder.rfind('/') + 1:]
        print label
        for filename in ([x for x in os.listdir(subfolder) if x.endswith('.wav')][-2:]):
            try:
                result = recognize(subfolder+'/'+filename)
                print '\t' + filename + ' ' + result + ' ' + str((result==label))
            except:
                print '\t' + filename + ' error'
                pass

