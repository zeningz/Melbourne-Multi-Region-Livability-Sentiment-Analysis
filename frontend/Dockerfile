FROM node:16.15.0

EXPOSE 3000

# WORKDIR /usr/src/app

COPY src src

COPY public public

COPY package.json package.json

COPY ".env.local" ".env.local"

RUN npm install --save --force
RUN npm install react-scripts -g

CMD ["npm", "start"]