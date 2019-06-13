from lane_change_risk_detection.dataset import DataSet
from lane_change_risk_detection.models import Models
from keras.models import load_model, Model
from lane_change_risk_detection.dataset import *
from Mask_RCNN.mask_rcnn.detect_objects import DetectObjects


dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)

# image_path = os.path.join(dir_name, 'data/input/')
# masked_image_path =os.path.join(dir_name, 'data/masked_images/')
#
# masked_image_extraction = DetectObjects(image_path, masked_image_path)
# masked_image_extraction.save_masked_images()

class_weight = {0: 0.05, 1: 0.95}
training_to_all_data_ratio = 0.9
nb_cross_val = 1
nb_epoch = 1000
batch_size = 32

masked_image_path = '/media/ekim-hpc/hdd1/data/1000_Lane_change/markRCNN_processed_images'

data = DataSet()
data.read_video(masked_image_path, option='fixed frame amount', number_of_frames=50, scaling='scale', scale_x=0.1, scale_y=0.1)
data.save(save_dir=dir_name)
data.read_risk_data("LCTable.csv")
data.convert_risk_to_one_hot(risk_threshold=0.05)

Data = data.video
label = data.risk_one_hot

model = Models(nb_epoch=nb_epoch, batch_size=batch_size, class_weights=class_weight)
model.build_cnn_to_lstm_model(input_shape=Data.shape[1:])
model.train_n_fold_cross_val(Data, label, training_to_all_data_ratio=training_to_all_data_ratio, n=nb_cross_val, print_option=0, plot_option=0, save_option=0)
model.model.save('maskRCNN_CNN_lstm.h5')
