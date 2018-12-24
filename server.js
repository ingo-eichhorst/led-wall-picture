
const Koa = require('koa');
const app = module.exports = new Koa();
const Router = require('koa-router');
const router = new Router();
const { spawn } = require('child_process');
let picProgram

async function switchPic(mode) {
  if (picProgram) picProgram.kill('SIGHUP');
  picProgram = spawn('python',['picture.py','--' + mode]);
}

router.get('/switch/:mode', (ctx, next) => {
  return switchPic(ctx.params.mode)
});

app.use(require('koa-static')('./', {}));

app
  .use(router.routes())
  .use(router.allowedMethods())
  .listen(5000)
