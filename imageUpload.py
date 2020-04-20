#pip install boto3

import boto3

s3 = boto.resource('s3')

# create bucket in s3, 'name' refers to the name of bucket
imgBucket = s3.Bucket('NAME')

# initialize folder for current user
var userFolder = (userID) + '/'
var profileFolder = userFolder + 'profile_pic/'
var bannerFolder = userFolder + 'banner/'
var imageFolder = userFolder + 'images/'

# folderKey is the folder we want to access
var folderKey = 'profileFolder | bannerFolder | imageFolder'

# deletes the content of the folder
# on account creation, these folders will hold default images
# when the user wants to change their image, the old one will be deleted and replaced with the new one
imgBucket.delete_objects(
    Delete={
        'Objects':
        [
            {
                'Key' : folderKey
                
            }
        ]
    }
)

# stores user's uploaded image into bucket
imgBucket.put_object(Body='IMG_FILENAME', Key=folderKey)
