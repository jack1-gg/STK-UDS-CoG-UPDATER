
# STK-UDS-CoG-UPDATER
Web-app to update STK CoG from UDS. Tool compatible with UDS (Ultimate Deal Sheet), or any other sheet with the same fields. 

Live app: https://stk-uds-cog-updater.herokuapp.com/

Repo connected to Heroku and automatic deploys enabled.

## How to use
Short guide if you want to use the live web-app.

 1. Create and download "Cost of Goods - Update List" on STK. (Reports > + > Cost of Goods - Update List)
 2. Download UDS "Deal Sheet" sheet as csv. ("Deal Sheet" > File > Download > Comma-separated values (.csv))
 3. Drang files or click to upload.
 4. Click submit.
 5. You'll get you updated CoG List back :)

## How to run
Short guide if you want to run the software yourself.
 1. Install required modules `pip install -r requirements.txt`
 2. Run wsgi.py `python wsgi.py`
 3. Follow How to use steps