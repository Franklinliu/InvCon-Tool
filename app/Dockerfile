FROM node:16

WORKDIR /usr/src/app/my-app

COPY package.json ./

COPY *.js ./

COPY src ./src

COPY public ./public

RUN npm install -g npm@8.10.0

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "serve"]