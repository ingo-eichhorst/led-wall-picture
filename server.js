
const Koa = require('koa');
const app = module.exports = new Koa();
const Router = require('koa-router');
const router = new Router();
const { spawn } = require('child_process');
let picProgram

async function switchPic(mode) {
  if (picProgram) picProgram.kill('SIGHUP');
  console.log('Spawn process: python picture.py --' + mode)

  picProgram = spawn('python',['picture.py','--' + mode]);
  picProgram.stdout.on('data', (data) => {
    console.log(data.toString());
  });
  picProgram.stderr.on('data', (data) => {
    console.log(`stderr: ${data.toString()}`);
  });
  picProgram.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
}

router.get('/switch/:mode', (ctx, next) => {
  return switchPic(ctx.params.mode)
});

app.use(require('koa-static')('./', {}));

app
  .use(router.routes())
  .use(router.allowedMethods())
  .listen(5000)

console.log('Started server on port 5000')
switchPic('simulate')
console.log('Set pic in simulation mode')