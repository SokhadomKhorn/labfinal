const mongoose = require('mongoose');

// The connection string comes from the environment:
// - locally from the .env file (not committed)
// - in Kubernetes from the "mongodb-secret" Secret
async function connectDB() {
  const uri = process.env.MONGODB_URI;
  if (!uri) {
    console.error('MONGODB_URI is not set');
    process.exit(1);
  }
  try {
    await mongoose.connect(uri, { dbName: process.env.MONGODB_DATABASE || 'student_management' });
    console.log('Connected to MongoDB');
  } catch (err) {
    console.error('MongoDB connection error:', err.message);
    process.exit(1);
  }
}

module.exports = connectDB;
