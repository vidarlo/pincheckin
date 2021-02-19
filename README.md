# pincheckin

To run with Docker
'''
docker build . -t pincheckin
docker run -v /tmp/data:/data -p 5000:5000 -e "TZ=Europe/Oslo"  pincheckin
'''

`/tmp/data` must exist for above command to work. Database will be stored in this location. It will be created if it does not exist.