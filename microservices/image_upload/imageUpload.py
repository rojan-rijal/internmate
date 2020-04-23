
import boto3


# this function stores the user's image into an s3 bucket
# 	bucketName is the name of the image bucket in s3
# 	userID is current user's id
# 	imgName is the image file the user chose
# 	folderName is the name of the folder the image should go into (profile_pic, banner, images)
def storeImage(bucketName, userID, imgName, folderName):
	
	s3 = boto.resource('s3')

	# access bucket in s3, 'name' refers to the name of bucket
	imgBucket = s3.Bucket(bucketName)

	# create the ID of the folder we want to access
	var folderKey = userID + '/' + folderName

	# delete the current content of the folder
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

	# store user's uploaded image into bucket
	imgBucket.put_object(Body=imgName, Key=folderKey)

# this function returns the image from an s3 bucket
# 	bucketName is the name of the image bucket in s3
# 	userID is current user's id
# 	folderName is the name of the folder the image should go into (profile_pic, banner, images)
def getImage(bucketName, userID, folderName):
	
	s3 = boto.resource('s3')

	# create the ID of the folder we want to access
	var folderKey = userID + '/' + folderName	
	
	# extract object from the s3 bucket
	obj = s3.Object(bucketName, folderKey)

	# get the content of the object (stored in 'Body')
	image = obj.get()['Body'].read()

	return image
