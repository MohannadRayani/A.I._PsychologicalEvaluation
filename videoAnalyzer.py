from fer import Video
from fer import FER

def videoAnalyzerMain(questionID):
    # Put in the location of the video file that has to be processed
    try:
        location_videofile = "content/videos/Question{}.mp4".format(questionID)

        # Build the Face detection detector
        face_detector = FER(mtcnn=True)
        # Input the video for processing
        input_video = Video(location_videofile)

        # The Analyze() function will run analysis on every frame of the input video.
        # It will create a rectangular box around every image and show the emotion values next to that.
        # Finally, the method will publish a new video that will have a box around the face of the human with live emotion values.
        processing_data = input_video.analyze(face_detector, display=False)

        # We will now convert the analysed information into a dataframe.
        # This will help us import the data as a .CSV file to perform analysis over it later
        vid_df = input_video.to_pandas(processing_data)
        vid_df = input_video.get_first_face(vid_df)
        vid_df = input_video.get_emotions(vid_df)

        # We will now work on the dataframe to extract which emotion was prominent in the video
        angry = sum(vid_df.angry)
        disgust = sum(vid_df.disgust)
        fear = sum(vid_df.fear)
        happy = sum(vid_df.happy)
        sad = sum(vid_df.sad)
        surprise = sum(vid_df.surprise)
        neutral = sum(vid_df.neutral)

        emotions_values = {'Angry':angry, 'Disgust':disgust, 'Fear':fear, 'Happy':happy, 'Sad':sad, 'Surprise':surprise}

        mostCommonEmotion = max(emotions_values, key=emotions_values.get)
        if mostCommonEmotion == 'Neutral':
            mostCommonEmotion = emotions_values
        # print('Most common emotion was: {}'.format(mostCommonEmotion))

        if mostCommonEmotion  in ['Angry', 'Disgust', 'Fear', 'Sad']:
            return mostCommonEmotion, 'Negative'
        else:
            return mostCommonEmotion, 'Positive'
    except:
        return 'Task Failed', 'Negative'