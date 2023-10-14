import fs from 'fs';
import { loadJson } from './helper.js';


// Demo sample data
const filepath = 'src/data.json';
const todos = loadJson(filepath);


const db = { todos };

export { db as default };