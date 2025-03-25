let suggestionsVisible = true;

function createModal() {
    const modal = document.createElement('div');
    modal.id = 'imageModal';
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img id="modalImage" src="" alt="Full Size Image">
        </div>
    `;
    document.body.appendChild(modal);

    modal.querySelector('.close-modal').onclick = () => modal.style.display = 'none';
    modal.onclick = (e) => {
        if (e.target === modal) modal.style.display = 'none';
    };
}

document.addEventListener('DOMContentLoaded', createModal);

function addMessage(message, isUser) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'support-message'}`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    const avatarIcon = document.createElement('i');
    avatarIcon.className = isUser ? 'fas fa-user' : 'fas fa-shoe-prints';
    avatarDiv.appendChild(avatarIcon);
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    if (!isUser && message.includes('[SHOW_PRODUCT]')) {
        const cleanMessage = message.replace('[SHOW_PRODUCT]', '');
        
        const messagePara = document.createElement('p');
        messagePara.textContent = cleanMessage;
        messageContent.appendChild(messagePara);
        
        const shoeImg = document.createElement('img');
        shoeImg.src = "/static/images/gt_cut2.jpg";
        shoeImg.alt = "GT Cut 2";
        shoeImg.className = 'product-image clickable';
        
        shoeImg.onclick = function() {
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImage');
            modal.style.display = 'block';
            modalImg.src = this.src;
        };
        
        messageContent.appendChild(shoeImg);
    } else if (!isUser && message.toLowerCase().includes('size guide')) {
        const messagePara = document.createElement('p');
        messagePara.textContent = "Here's our size guide to help you find your perfect fit:";
        messageContent.appendChild(messagePara);
        
        const sizeGuideImg = document.createElement('img');
        sizeGuideImg.src = "/static/images/size.png";
        sizeGuideImg.alt = "Shoe Size Guide";
        sizeGuideImg.className = 'size-guide-image clickable';
        
        sizeGuideImg.onclick = function() {
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImage');
            modal.style.display = 'block';
            modalImg.src = this.src;
        };
        
        messageContent.appendChild(sizeGuideImg);
    } else {
        const messagePara = document.createElement('p');
        messagePara.textContent = message;
        messageContent.appendChild(messagePara);
    }
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function toggleSuggestions() {
    const suggestionBox = document.getElementById('suggestionBox');
    suggestionsVisible = !suggestionsVisible;
    suggestionBox.style.display = suggestionsVisible ? 'flex' : 'none';
}

function selectSuggestion(suggestion) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = suggestion;
    sendMessage(); // Automatically send the message when a suggestion is clicked
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (message) {
        addMessage(message, true);
        messageInput.value = '';
        suggestionsVisible = false;
        document.getElementById('suggestionBox').style.display = 'none';
        
        try {
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            addMessage(data.response, false);
            
            setTimeout(() => {
                suggestionsVisible = true;
                document.getElementById('suggestionBox').style.display = 'flex';
            }, 1000);
            
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your message.', false);
        }
    }
}

document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

document.getElementById('suggestionBox').style.display = 'flex';