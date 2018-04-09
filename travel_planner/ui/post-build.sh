#!/bin/bash
echo "Start building web UI"

# Move index.html to django templates folder
mv -f ./build/index.html /ui_dist/templates/index.html

# Move static files out to build folder
mv -f ./build/static/css ./build
mv -f ./build/static/js ./build
mv -f ./build/static/media ./build

# Remove empty static folder
rm -rf ./build/static

# Copy build files to main project root
cp -r -u ./build /ui_dist