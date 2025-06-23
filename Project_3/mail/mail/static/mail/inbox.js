document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  document.querySelector('#compose-form').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}




function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  const view = document.querySelector('#emails-view');
  view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  // Fetching emails & rendering them as a list
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    emails.forEach(email => {
      
      const emailDiv = document.createElement('div');
      emailDiv.className = 'email-box';
      emailDiv.style.border = '1px solid #ccc';
      emailDiv.style.padding = '10px';
      emailDiv.style.margin = '5px 0';
      emailDiv.style.cursor = 'pointer';

      emailDiv.style.backgroundColor = email.read ? '#f0f0f0' : 'white';

      // What to show (From or To 's email)
      const titleEmail = mailbox == 'sent'
        ? `To: ${email.recipients.join(', ')}`
        : `From: ${email.sender}`;

      emailDiv.innerHTML = `
        <span><strong>${titleEmail}</strong></span>
        <span>${email.subject}</span>
        <span style="float: right;">${email.timestamp}</span>
      `;


      emailDiv.addEventListener('click', () => view_email(email.id));

      view.appendChild(emailDiv);

    });
  });
}



function send_mail(event) {

  event.preventDefault();

  // Getting details from the form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;


  // Sending the request to the server

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({ 

      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);

    load_mailbox('sent');
  });
}





function view_email(id) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  const emailView = document.querySelector('#email-view');

  emailView.style.display = 'block';

  emailView.innerHTML = '';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log('View of email:', email);
        

    // Marking as read by changing 'read' value
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ read: true })
    });

    const content = document.createElement('div');

    content.innerHTML = `
      <p><strong>From:</strong> ${email.sender}</p>
      <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
      <p><strong>Subject:</strong> ${email.subject}</p>
      <p><strong>Timestamp:</strong> ${email.timestamp}</p>
    `;

    emailView.appendChild(content);


    // .innerText because of jinja template string
    if(email.sender !== document.querySelector('h2').innerText) {

      console.log('hello');
      const archiveBtn = document.createElement('button');
      archiveBtn.className = 'btn btn-sm btn-outline-primary';
      archiveBtn.innerHTML = email.archived ? 'Unarchive' : 'Archive';

      archiveBtn.addEventListener('click', () => {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({ archived: !email.archived })
        })
        .then( () => load_mailbox('inbox'));
      });

      emailView.appendChild(archiveBtn);
    }

    const bodyOfEmail = document.createElement('div');
    bodyOfEmail.innerHTML = `
      <hr>
      <p>${email.body.replace(/\n/g, '<br>')}</p>
    `;

    emailView.appendChild(bodyOfEmail);
  });
}