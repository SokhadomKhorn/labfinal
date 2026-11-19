// Prints the live MongoDB Atlas data (students + counters) from inside the cluster.
// Usage (PowerShell):
//   Get-Content scripts\show-db.js | kubectl exec -i gateway-registration-pod -c registration-service -- node -
const mongoose = require('/app/node_modules/mongoose');

(async () => {
  await mongoose.connect(process.env.MONGODB_URI, { dbName: process.env.MONGODB_DATABASE || 'student_management' });
  const db = mongoose.connection.db;
  console.log(`Connected to MongoDB Atlas host: ${mongoose.connection.host}`);
  console.log(`Database: ${db.databaseName}\n`);

  const students = await db.collection('students').find().sort({ Student_id: 1 }).toArray();
  console.log(`== Collection: students (${students.length} documents) ==`);
  for (const s of students) console.log(JSON.stringify(s, null, 2));

  const counters = await db.collection('counters').find().toArray();
  console.log(`\n== Collection: counters (${counters.length} documents) ==`);
  for (const c of counters) console.log(JSON.stringify(c, null, 2));

  await mongoose.disconnect();
})().catch((e) => { console.error(e.message); process.exit(1); });
