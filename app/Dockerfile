FROM node:16

WORKDIR /usr/src/app/my-app

COPY package.json ./

RUN npm install -g npm@8.10.0

RUN npm install

COPY *.js ./

COPY src ./src

COPY public ./public

EXPOSE 3000

CMD ["npm", "run", "serve"]