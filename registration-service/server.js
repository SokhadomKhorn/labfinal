// Registration Microservice
// Runs in Pod 1 next to the API Gateway (reached by the gateway on localhost:5001)
const express = require('express');
const bcrypt = require('bcryptjs');
const connectDB = require('./db');
const Student = require('./student_schema');
const Counter = require('./counter_schema');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 5001;

// Generates the next Student_id: 1, 2, 3, ...
async function nextStudentId() {
  const counter = await Counter.findByIdAndUpdate(
    'Student_id',
    { $inc: { seq: 1 } },
    { new: true, upsert: true }
  );
  return counter.seq;
}

// Never send the password back to the client
function publicView(student) {
  const s = student.toObject();
  delete s.student_password;
  delete s._id;
  delete s.__v;
  return s;
}

app.get('/health', (req, res) => {
  res.json({ service: 'registration-service', status: 'UP' });
});

// REGISTER A STUDENT
// POST /api/register
// { "student_name": "...", "student_mobile": "...", "student_email": "...", "student_password": "..." }
app.post('/api/register', async (req, res) => {
  console.log('REGISTRATION API EXECUTED');
  const { student_name, student_mobile, student_email, student_password } = req.body || {};

  if (!student_name || !student_mobile || !student_email || !student_password) {
    return res.status(400).json({
      message: 'student_name, student_mobile, student_email and student_password are required'
    });
  }

  try {
    const exists = await Student.findOne({ student_email: student_email.toLowerCase() });
    if (exists) {
      return res.status(409).json({ message: 'A student with this email is already registered' });
    }

    const student = new Student({
      Student_id: await nextStudentId(),
      Student_name: student_name,
      student_mobile: String(student_mobile),
      student_email: student_email,
      student_password: await bcrypt.hash(String(student_password), 10)
    });

    const saved = await student.save();
    res.status(201).json({
      message: 'Student registered successfully',
      student: publicView(saved)
    });
  } catch (err) {
    console.error('Registration error:', err.message);
    res.status(500).json({ message: err.message || 'Error while registering student' });
  }
});

// LIST ALL STUDENTS (used to check results after registering / updating)
// GET /api/students
app.get('/api/students', async (req, res) => {
  try {
    const students = await Student.find().sort({ Student_id: 1 });
    res.json(students.map(publicView));
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// GET ONE STUDENT
// GET /api/students/:id
app.get('/api/students/:id', async (req, res) => {
  try {
    const student = await Student.findOne({ Student_id: Number(req.params.id) });
    if (!student) return res.status(404).json({ message: 'Student not found' });
    res.json(publicView(student));
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

connectDB().then(() => {
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Registration Service running on port ${PORT}`);
  });
});
