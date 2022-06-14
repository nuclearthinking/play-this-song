rm -rf app/static/*
cd frontend
yarn run build
mv build/static/css ../app/static/css
mv build/static/js ../app/static/js
mv build/static/media ../app/static/media
rm -rf build/static
mv -v build/* ../app/static/
git add ../app/static