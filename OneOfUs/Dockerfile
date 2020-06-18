FROM node:10.15.3-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm set strict-ssl false

RUN npm install

COPY ./src/ ./

EXPOSE 3001

CMD npm run start