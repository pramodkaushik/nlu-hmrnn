from hmlstm import HMLSTMNetworkQa, CBTDataset
import argparse

# hyper parameters
INPUT_EMBED_SIZE = 384
NUM_LAYER = 2
HIDDEN_STATE_SIZES = 256
LEARNING_RATE = 1e-3
OUT_HIDDEN_STATE_SIZES = 1024

# constants
VOCABULARY_PATH = './CBTest/vocab/CBT_CN_vocab.txt'
TRAIN_DATA_PATH = './CBTest/data/cbtest_CN_train.txt'
VALID_DATA_PATH = './CBTest/data/cbtest_CN_valid_2000ex.txt'
TEST_DATA_PATH = './CBTest/data/cbtest_CN_test_2500ex.txt'
CANDIDATE_NUM = 10
BATCH_SIZE = 32
SHOW_STAT_AFTER_STEP = 50
VALID_AFTER_STEP = 300
EPOCHS = 3

# parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("--dev", help="help catch bug early by running a subset of data",
                    action="store_true")
parser.add_argument("--predict", help="use trained network to predict",
                    action="store_true")
args = parser.parse_args()

if args.dev:
    TRAIN_DATA_PATH = './CBTest/data/cbtest_CN_quick_dev_6ex.txt'
    VALID_DATA_PATH = TRAIN_DATA_PATH
    BATCH_SIZE = 2
    VALID_AFTER_STEP = 3
    SHOW_STAT_AFTER_STEP = 1
    EPOCHS = 3

# Prepare dataset
cbt = CBTDataset(vocab_path=VOCABULARY_PATH, batch_size=BATCH_SIZE)
train_dataset = cbt.prepare_dataset(TRAIN_DATA_PATH, name='train') # return a tf.data.Dataset instance
valid_dataset = cbt.prepare_dataset(VALID_DATA_PATH, name='valid')

# Prepare network
network = HMLSTMNetworkQa(
        input_size=INPUT_EMBED_SIZE,
        output_size=CANDIDATE_NUM,
        num_layers=NUM_LAYER, 
        hidden_state_sizes=HIDDEN_STATE_SIZES,
        out_hidden_size=OUT_HIDDEN_STATE_SIZES,
        embed_size=INPUT_EMBED_SIZE,
        learning_rate=LEARNING_RATE,  
        task='classification')

if not args.predict:
    # Training
    network.train(cbt, train_dataset, valid_dataset, save_vars_to_disk=True, 
                  load_vars_from_disk=False, variable_path='./qa_variable_1e-3',
                  valid_after_step=VALID_AFTER_STEP, show_stat_after_step=SHOW_STAT_AFTER_STEP, epochs=EPOCHS)
# else:
    # Predicting

"""
predictions = network.predict(batches_in[-1], variable_path='./text8')
boundaries = network.predict_boundaries(batches_in[-1], variable_path='./text8')

# visualize boundaries
viz_char_boundaries(get_text(batches_out[-1][0]), get_text(predictions[0]), boundaries[0])
"""