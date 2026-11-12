// Update Microservice - update student mobile number or password
// Runs in Pod 2 (reached by the API Gateway through the "update-service" Kubernetes Service)
const express = require('express');
const bcrypt = require('bcryptjs');
const connectDB = require('./db');
const Student = require('./student_schema');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 5002;

function publicView(student) {
  const s = student.toObject();
  delete s.student_password;
  delete s._id;
  delete s.__v;
  return s;
}

function isValidMobile(mobile) {
  return /^\+?[0-9]{8,15}$/.test(String(mobile).replace(/[\s-]/g, ''));
}

app.get('/health', (req, res) => {
  res.json({ service: 'update-service', status: 'UP' });
});

// UPDATE MOBILE NUMBER
// PUT /api/update/mobile/:id    { "student_mobile": "..." }
app.put('/api/update/mobile/:id', async (req, res) => {
  console.log('UPDATE MOBILE API EXECUTED');
  const { student_mobile } = req.body || {};
  if (!student_mobile) {
    return res.status(400).json({ message: 'student_mobile is required' });
  }
  if (!isValidMobile(student_mobile)) {
    return res.status(400).json({ message: 'student_mobile must be 8 to 15 digits' });
  }

  try {
    const student = await Student.findOneAndUpdate(
      { Student_id: Number(req.params.id) },
      { $set: { student_mobile: String(student_mobile) } },
      { new: true }
    );
    if (!student) return res.status(404).json({ message: 'Student not found' });
    res.json({ message: 'Mobile number updated successfully', student: publicView(student) });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// UPDATE PASSWORD
// PUT /api/update/password/:id  { "student_password": "..." }
app.put('/api/update/password/:id', async (req, res) => {
  console.log('UPDATE PASSWORD API EXECUTED');
  const { student_password } = req.body || {};
  if (!student_password) {
    return res.status(400).json({ message: 'student_password is required' });
  }
  if (String(student_password).length < 6) {
    return res.status(400).json({ message: 'student_password must be at least 6 characters' });
  }

  try {
    const hashed = await bcrypt.hash(String(student_password), 10);
    const student = await Student.findOneAndUpdate(
      { Student_id: Number(req.params.id) },
      { $set: { student_password: hashed } },
      { new: true }
    );
    if (!student) return res.status(404).json({ message: 'Student not found' });
    res.json({ message: 'Password updated successfully', student: publicView(student) });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// UPDATE MOBILE AND/OR PASSWORD IN ONE CALL
// PATCH /api/update/:id  { "student_mobile": "...", "student_password": "..." }  (either or both)
app.patch('/api/update/:id', async (req, res) => {
  console.log('UPDATE STUDENT API EXECUTED');
  const { student_mobile, student_password } = req.body || {};
  if (!student_mobile && !student_password) {
    return res.status(400).json({ message: 'Send student_mobile, student_password, or both' });
  }

  const changes = {};
  if (student_mobile) {
    if (!isValidMobile(student_mobile)) {
      return res.status(400).json({ message: 'student_mobile must be 8 to 15 digits' });
    }
    changes.student_mobile = String(student_mobile);
  }
  if (student_password) {
    if (String(student_password).length < 6) {
      return res.status(400).json({ message: 'student_password must be at least 6 characters' });
    }
    changes.student_password = await bcrypt.hash(String(student_password), 10);
  }

  try {
    const student = await Student.findOneAndUpdate(
      { Student_id: Number(req.params.id) },
      { $set: changes },
      { new: true }
    );
    if (!student) return res.status(404).json({ message: 'Student not found' });
    res.json({
      message: 'Student updated successfully',
      updated_fields: Object.keys(changes),
      student: publicView(student)
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

connectDB().then(() => {
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Update Service running on port ${PORT}`);
  });
});
