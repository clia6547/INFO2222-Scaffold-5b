document.addEventListener('DOMContentLoaded', () => {
    const articleList = document.getElementById('article-list');
    const commentList = document.getElementById('comment-list');
    const userList = document.getElementById('user-list');
    
    const articleTemplate = document.getElementById('article-template').content;
    const commentTemplate = document.getElementById('comment-template').content;
    const userTemplate = document.getElementById('user-template').content;

    // Mock data for articles, comments, and users
    const articles = [
        { title: "Article 1", content: "Content of article 1", author: "Staff" },
        { title: "Article 2", content: "Content of article 2", author: "Student" }
    ];

    const comments = [
        { content: "This is a comment on article 1", author: "Student" },
        { content: "This is another comment on article 1", author: "Staff" }
    ];

    const users = [
        { name: "User 1", role: "Student" },
        { name: "User 2", role: "Staff" }
    ];

    // Load articles
    articles.forEach(article => {
        const articleClone = document.importNode(articleTemplate, true);
        articleClone.querySelector('.article-title').textContent = article.title;
        articleClone.querySelector('.article-content').textContent = article.content;
        articleClone.querySelector('.article-author').textContent = article.author;
        articleList.appendChild(articleClone);
    });

    // Load comments
    comments.forEach(comment => {
        const commentClone = document.importNode(commentTemplate, true);
        commentClone.querySelector('.comment-content').textContent = comment.content;
        commentClone.querySelector('.comment-author').textContent = comment.author;
        commentList.appendChild(commentClone);
    });

    // Load users
    users.forEach(user => {
        const userClone = document.importNode(userTemplate, true);
        userClone.querySelector('.user-name').textContent = user.name;
        userList.appendChild(userClone);
    });

    // Event listeners for article buttons
    document.querySelectorAll('.edit-article-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Edit article functionality
        });
    });

    document.querySelectorAll('.delete-article-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Delete article functionality
        });
    });

    // Event listeners for comment buttons
    document.querySelectorAll('.delete-comment-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Delete comment functionality
        });
    });

    // Event listeners for user buttons
    document.querySelectorAll('.mute-user-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Mute/unmute user functionality
        });
    });
});
