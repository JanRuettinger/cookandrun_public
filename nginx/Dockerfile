FROM nginx:1.11.3
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY cookandrun_organizer_app.conf /etc/nginx/conf.d/
COPY cookandrun_participant_app.conf /etc/nginx/conf.d/

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim-tiny"]
