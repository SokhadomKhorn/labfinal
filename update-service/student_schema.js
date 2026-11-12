const mongoose = require('mongoose');

// Database schema:
// Student_id, Student_name, student_mobile, student_email, student_password
const StudentSchema = new mongoose.Schema(
  {
    Student_id: { type: Number, required: true, unique: true },
    Student_name: { type: String, required: true, trim: true },
    student_mobile: { type: String, required: true, trim: true },
    student_email: { type: String, required: true, unique: true, lowercase: true, trim: true },
    student_password: { type: String, required: true }
  },
  { timestamps: true }
);

module.exports = mongoose.model('Student', StudentSchema, 'students');
