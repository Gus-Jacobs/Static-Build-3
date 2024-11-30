# Static-Build-3
Developed by Gus Jacobs 
Some of the intial work was taken from FreeCodeCamp's tutorial
Final attempt at a social media website built in 2023. Purpose of this project was to make a fully functional webpage that acted like a social media page, allowing users to upload videos and pictures as well as post text. The key problems were setting file size and type restriction and showing that error message, the key problem with this was blocking the file upload before the file was even uploaded, this required the file to be checked for size and type and return an error. Another problem was storage space, since it was pointless to save every profile picture and background when they were changed or deleted they were also delete from the django database and the file was removed thus clearing up space. similarly with posts when they are deleted they are removed from the database entirely, this clearing space. 

