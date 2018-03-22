FROM node:8.9.4

RUN mkdir /ui_source /ui_dist

COPY ./travel_planner /ui_source
COPY ./post-build.sh /ui_source

WORKDIR /ui_source
RUN ls -lah
RUN npm install && npm run build

RUN chmod +x ./post-build.sh

ENTRYPOINT [ "./post-build.sh" ]
