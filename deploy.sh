#!/bin/bash

# NetAI Insights Deployment Script
# Author: Glevin

echo "🚀 Deploying NetAI Insights..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    exit 1
fi

# Deploy to GitHub
echo "📦 Pushing to GitHub..."
git add .
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo "✅ GitHub deployment complete!"

# Optional: Deploy to Render/Heroku
echo "🌐 Would you like to deploy to Render? (y/n)"
read -r deploy_choice

if [[ "$deploy_choice" == "y" || "$deploy_choice" == "Y" ]]; then
    echo "Deploying to Render..."
    # Add Render deployment commands here
fi

echo "🎉 Deployment process completed!"
echo "📊 Live Demo: https://your-deployment-link"
echo "📚 API Docs: https://your-deployment-link/api/docs"