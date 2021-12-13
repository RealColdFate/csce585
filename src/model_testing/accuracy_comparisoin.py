import itertools
from tensorflow.keras.models import load_model
import numpy as np
import json
from sklearn.metrics import confusion_matrix
import os
import pandas as pd
import matplotlib.pyplot as plt

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
NAME_LABELS = ['song0', 'song1', 'song2', 'song3', 'song4', 'song5', 'song6', 'song7', 'song8', 'song9', 'song10',
               'song11', 'song12', 'song13', 'song14', 'song15', 'song16', 'song17', 'song18', 'song19']
NAME_LABELS = sorted(NAME_LABELS)
print(NAME_LABELS)

GLOBAL_NORMALIZE = True


def save_features_to_json(data: list, export_path: str) -> None:
    """
    Writes data given to json file with path provided
    this will not work if data object passed is not json serializable
    :param data: list
    :param export_path: str
    """
    with open(export_path, 'w') as f:
        json.dump(data, f)


def get_files_from_parent(parent_dir):
    paths = []
    for sub in os.listdir(parent_dir):
        sub_dir = os.path.join(parent_dir, sub)
        for f in os.listdir(sub_dir):
            paths.append(os.path.join(sub_dir, f))

    return paths


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Reds):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def main() -> None:
    model_path = "../model_training/models/FF_DNN_OV_V_2.h5"
    overlay_parent_dir = "../../data/segmented_songs/sample_dict_of_20_songs_0_overlay_segment_mfccs/"
    current_model = load_model(model_path)

    file_paths = get_files_from_parent(overlay_parent_dir)
    y_true = []
    y_pred = []
    correct = 0
    for f in file_paths:
        obj = read_in_feature_from_json(f)
        answer = obj[1]
        guess = give_guess(current_model, f)
        y_true.append(answer)
        y_pred.append(guess)
        if guess == answer:
            correct += 1

    cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
    plot_confusion_matrix(cm=cm, classes=NAME_LABELS, title="Overlay vs Normalized Overlay")
    plt.show()
    print(f"# correct :{correct} %correct: {correct / len(y_true)}")


def read_in_feature_from_json(file_path: str) -> list:
    with open(file_path, 'r') as f:
        feature = f.readlines()
        feature = json.loads(feature[0])
        class_label = feature[1]
        features = np.array(feature[0])
        feature = [features, class_label]
    return feature


def find_readable_predictions(predictions, labels):
    index = predictions[0].tolist().index(max(predictions[0]))
    return labels[index]


def give_guess(model, input_path):
    labeled_input = read_in_feature_from_json(input_path)

    model_input = labeled_input[0]

    if GLOBAL_NORMALIZE:
        df = pd.DataFrame(labeled_input[0])
        z_score_normalized_mfccs = (df.values - df.values.mean()) / df.values.std()
        z_score_normalized_mfccs = np.array([i[0] for i in z_score_normalized_mfccs])
        model_input = z_score_normalized_mfccs

    feature_arr = np.array([model_input])
    numpy_arr_predictions = model.predict(feature_arr)
    return find_readable_predictions(numpy_arr_predictions, NAME_LABELS)


if __name__ == "__main__":
    main()
