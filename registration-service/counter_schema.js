const mongoose = require('mongoose');

// Keeps the last used Student_id so each new student gets the next number
const CounterSchema = new mongoose.Schema({
  _id: { type: String, required: true },
  seq: { type: Number, default: 0 }
});

module.exports = mongoose.model('Counter', CounterSchema, 'counters');
