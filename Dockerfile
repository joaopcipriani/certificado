# Use lightweight Nginx image
FROM nginx:alpine

# Copy static files to Nginx web root
COPY public /usr/share/nginx/html

# Expose port 80
EXPOSE 80
