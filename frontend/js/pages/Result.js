
import { displayTables } from "../display/DisplayTables.js";
import { displayQuery } from "../display/DisplayQuery.js";
import { displayArrows } from "../display/DrawArrows.js";

const stored = sessionStorage.getItem('querySession');
if (!stored) { location.href = '/input'; }

const parsed = JSON.parse(stored);
const query = parsed.query;
const subqueries = parsed.subqueryResults;

displayQuery(query);
displayTables(subqueries);
displayArrows(subqueries);