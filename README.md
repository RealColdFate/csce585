# csce585
CSCE 585 AI project


# Project Setup 

The first thing you will need to do is get a map of songs, you may do this by either using  [provided song maps](https://github.com/RealColdFate/csce585/tree/main/src/data_processing/sample_dicts)
or generate your own using [create_sample_song_map.py](https://github.com/RealColdFate/csce585/blob/main/src/data_processing/create_song_sample_map.py). 

Once you have chosen a song map to use [audio_file_downloader.py](https://github.com/RealColdFate/csce585/blob/main/src/data_processing/audio_file_downloader.py) to download the song locally you are responsible for any content you download onto your personal computer. 

The next thing you will have to do is generate the audio segments, can you guess which script does this? Then you may choose to generate the overlaid segments with [audio_overlay.py](https://github.com/RealColdFate/csce585/blob/main/src/data_processing/audio_overlay.py) you can edit segment length here as well.

Now that you have genrated the song segments you want you will have to check [generate_segment_mfccs.py](https://github.com/RealColdFate/csce585/blob/main/src/data_processing/generate_segment_mfccs.py) make sure the import path is correct for generating the MFCC vectors for your segments. You may also want to edit the export path for your MFCC vectors. One final consideration is to keep the data normalized the current script will normalize the data via z-scre normalization you may change this in your own implementation. Note that the provided FF_DNN_V_* and FF_DNN_OV_V_* models are not trained on normalized data.

Once your MFCC vectors have been generated and stored you may see [simple_feed_forward.ipynb](https://github.com/RealColdFate/csce585/blob/main/src/model_training/simple_feed_forward.ipynb) here you will again need to check the provided import and export paths to make sure you have given the correct path to your training data. at the end of this file you will need to change the model name if you wish to save your trained model. 

Once you have created a satisfactory model you may evaluate it using [accuracy_comparison.py](https://github.com/RealColdFate/csce585/blob/main/src/model_testing/accuracy_comparisoin.py) you will have to specify which model to load and which data to evalueate on make sure the testing data is in a valid format. The expected format is the same as examples that will be generated. 
