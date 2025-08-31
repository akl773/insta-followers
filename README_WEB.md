# Instagram Analytics Web Application

A modern web interface for the Instagram Follower Analyzer, built with Flask (backend) and React (frontend). This application provides a beautiful, interactive dashboard for analyzing your Instagram follower relationships and tracking changes over time.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 16+
- MongoDB (local or remote)
- Instagram account credentials

### Installation

1. **Clone and setup:**
```bash
git clone <your-repo>
cd instagramFollowers
chmod +x setup.sh
./setup.sh
```

2. **Configure environment:**
Update the `.env` file with your credentials:
```env
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=InstagramStat
EXCEPTION_NOT_FOLLOWING_BACK=username1,username2
```

3. **Start the application:**
```bash
# Terminal 1 - Start Flask backend
python app.py

# Terminal 2 - Start React frontend
cd frontend
npm run dev
```

4. **Access the application:**
- Frontend: http://localhost:3000
   - Backend API: http://localhost:5001

## 🏗️ Architecture

### Backend (Flask)
- **RESTful API** endpoints for data access
- **Session management** for Instagram authentication
- **MongoDB integration** for data persistence
- **CORS support** for frontend communication
- **Error handling** and validation

### Frontend (React + TypeScript)
- **Material-UI** for modern, responsive design
- **React Router** for navigation
- **Axios** for API communication
- **Recharts** for data visualization
- **Dark theme** for better user experience
- **TypeScript** for type safety

## 📊 Features

### Dashboard
- **Real-time statistics** for followers and following
- **Quick report generation** with one-click button
- **Recent changes analysis** showing new/lost followers
- **User activity overview** with profile pictures
- **Relationship breakdown** (mutual, followers only, following only)

### Reports
- **Historical report viewing** with detailed breakdowns
- **Change analysis** between consecutive reports
- **Export capabilities** for data analysis
- **Trend visualization** over time
- **Expandable accordion** for detailed user lists

### Not Following Back
- **List of users** who don't follow you back
- **Profile information** with avatars and names
- **Direct Instagram links** to user profiles
- **Exception handling** for specific usernames
- **Grid layout** for easy browsing

### Analytics
- **Growth trends** with line charts
- **Relationship distribution** with pie charts
- **Net follower changes** with bar charts
- **Detailed breakdowns** of new/lost followers
- **Summary statistics** with key metrics
- **Interactive charts** with tooltips and legends

## 🔌 API Endpoints

### Health & Status
- `GET /api/health` - Health check endpoint

### Data Retrieval
- `GET /api/followers?limit=10` - Get followers list
- `GET /api/following?limit=10` - Get following list
- `GET /api/reports?limit=20` - Get historical reports
- `GET /api/reports/latest` - Get most recent report
- `GET /api/not-following-back` - Get users not following back

### Data Generation
- `POST /api/reports/generate` - Generate new report

## 🎨 UI Components

### Navigation
- **Responsive navbar** with active page highlighting
- **Material-UI icons** for intuitive navigation
- **Breadcrumb-style** navigation structure

### Data Display
- **Card-based layouts** for clean information presentation
- **Data tables** with sorting and filtering
- **Charts and graphs** for visual data representation
- **Loading states** with spinners and skeletons
- **Error handling** with user-friendly messages

### Interactive Elements
- **Buttons** with loading states and icons
- **Chips** for status and category display
- **Avatars** for user profile pictures
- **Accordions** for expandable content
- **Tooltips** for additional information

## 🔒 Security Features

- **Session-based authentication** for Instagram
- **Environment variable** configuration
- **CORS protection** for API endpoints
- **Input validation** and sanitization
- **Error handling** without exposing sensitive data

## 📱 Mobile Support

The web application is fully responsive and works on:
- **Desktop browsers** (Chrome, Firefox, Safari, Edge)
- **Tablets** (iPad, Android tablets)
- **Mobile devices** (iPhone, Android phones)

## 🚀 Deployment

### Backend Deployment
```bash
# Using Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t instagram-analytics-backend .
docker run -p 5000:5000 instagram-analytics-backend
```

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy the dist/ folder to your web server
```

### Environment Variables for Production
```env
# Production settings
FLASK_ENV=production
MONGO_URI=mongodb://your-production-mongo-uri
DATABASE_NAME=InstagramStat
```

## 🔧 Development

### Backend Development
```bash
# Run in debug mode
python app.py

# Run with auto-reload
flask run --debug
```

### Frontend Development
```bash
cd frontend
npm run dev
# Vite will provide hot reload
```

### API Testing
```bash
# Test the API endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/reports/latest
```

### Database Management
```bash
# Connect to MongoDB
mongo
use InstagramStat
db.reports.find().sort({generated_at: -1}).limit(5)
```

## 📈 Performance Optimization

### Backend
- **Connection pooling** for MongoDB
- **Caching** for frequently accessed data
- **Bulk operations** for database updates
- **Query optimization** with indexes

### Frontend
- **Code splitting** for faster loading
- **Lazy loading** for components
- **Image optimization** for profile pictures
- **Bundle optimization** with Vite

## 🐛 Troubleshooting

### Common Issues

1. **Instagram Authentication Failed**
   - Check credentials in `.env` file
   - Ensure 2FA is disabled or use app passwords
   - Clear session files in `session/` directory

2. **MongoDB Connection Error**
   - Verify MongoDB is running
   - Check connection string in `.env`
   - Ensure database permissions

3. **Frontend Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility
   - Update dependencies: `npm update`

4. **API Connection Issues**
   - Verify backend is running on port 5000
   - Check CORS configuration
   - Ensure proxy settings in Vite config

### Debug Mode
```bash
# Backend debug
FLASK_ENV=development python app.py

# Frontend debug
cd frontend && npm run dev
```

## 📊 Data Structure

### Report Schema
```json
{
  "_id": "2024-01-15T00:00:00",
  "generated_at": "2024-01-15T00:00:00",
  "num_followers": 1500,
  "num_following": 800,
  "users": [
    {
      "id": "123456789",
      "username": "example_user",
      "full_name": "Example User",
      "profile_pic_url": "https://...",
      "type": ["follower", "following"]
    }
  ],
  "stats": {
    "new_followers_count": 5,
    "lost_followers_count": 2,
    "net_follower_change": 3
  }
}
```

## 🔮 Future Enhancements

- [ ] **Real-time notifications** for follower changes
- [ ] **Advanced analytics dashboard** with more metrics
- [ ] **Export to PDF/Excel** functionality
- [ ] **User authentication system** for multi-user support
- [ ] **Multi-account support** for managing multiple Instagram accounts
- [ ] **Email reports** with scheduled delivery
- [ ] **Mobile app** using React Native
- [ ] **Webhook integration** for real-time updates
- [ ] **Advanced filtering** and search capabilities
- [ ] **Custom dashboard** with drag-and-drop widgets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines
- Follow TypeScript best practices
- Use Material-UI components consistently
- Add proper error handling
- Include loading states
- Write meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Instagram API** for providing access to follower data
- **Material-UI** for the beautiful component library
- **Recharts** for the charting capabilities
- **Flask** for the robust backend framework
- **React** for the powerful frontend framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub
4. Check the logs for error messages

---

**Happy Instagram Analytics! 📊✨**
