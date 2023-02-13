const user_username = JSON.parse(document.getElementById('user-username').textContent);

document.querySelector('#chat-submit').onclick = function (e) {
  const messageInputDom = document.querySelector('#chat-input');
  const message = messageInputDom.value;
  chatSocket.send(JSON.stringify({
      'message': message,
      'username': user_username,
  }));
  messageInputDom.value = '';
};

const chat_id = JSON.parse(document.getElementById('chat-id-for-script').textContent);

const chatSocket = new WebSocket(
  'ws://' +
  window.location.host +
  '/ws/chat/' +
  chat_id +
  '/'
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  const old_messages = document.querySelector('#chat-text').value;
  document.querySelector('#chat-text').value = data.message+'\n' + old_messages;
}
