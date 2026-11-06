// The only module that reads content/. Every getter takes the bench id first, then the version.
import benchesDoc from "@content/benches.json";
import siteAbout from "@content/about.md?raw";
import fieldsDoc from "@content/fields.json";
import committeeDoc from "@content/committee.json";

import rcbVersions from "@content/rcb/versions.json";
import rcbBoard10 from "@content/rcb/1.0/leaderboard.json";
import rcbTasks10 from "@content/rcb/1.0/tasks.json";
import rcbAbout10 from "@content/rcb/1.0/about.md?raw";
import rcbAtlas10 from "@content/rcb/1.0/atlas.json";
import rcbPass510 from "@content/rcb/1.0/pass5.json";

import afeVersions from "@content/afe/versions.json";
import afeTasks10 from "@content/afe/1.0/tasks.json";
import afeAbout10 from "@content/afe/1.0/about.md?raw";

// Generated run files, keyed by bench then version then run_id.
const runFiles = import.meta.glob("@content/*/*/runs/*.json", { eager: true, import: "default" });
function runsOf(bench, version) {
  const prefix = `/${bench}/${version}/runs/`;
  return Object.fromEntries(
    Object.entries(runFiles).filter(([path]) => path.includes(prefix)).map(([, run]) => [run.run_id, run]),
  );
}

const books = {
  rcb: {
    versions: rcbVersions.versions,
    "1.0": {
      leaderboard: rcbBoard10,
      tasks: rcbTasks10,
      about: rcbAbout10,
      atlas: rcbAtlas10,
      pass5: rcbPass510,
      runs: runsOf("rcb", "1.0"),
    },
  },
  afe: {
    versions: afeVersions.versions,
    "1.0": {
      tasks: afeTasks10,
      about: afeAbout10,
      runs: {},
    },
  },
};

const book = (bench, version) => books[bench]?.[version];

export function getBenches() {
  return benchesDoc.benches;
}

export function getBench(id) {
  return getBenches().find((b) => b.id === id) || null;
}

export function getBenchSlots() {
  return benchesDoc.placeholders || 0;
}

// How many slides the home carousel shows in total (live benches first, placeholders fill the rest).
export function getCarouselSize() {
  return benchesDoc.carousel || getBenches().length + getBenchSlots();
}

export function getVersions(bench) {
  return books[bench]?.versions || [];
}

export function versionExists(bench, id) {
  return getVersions(bench).some((item) => item.id === id);
}

export function getVersion(bench, id) {
  return getVersions(bench).find((item) => item.id === id) || null;
}

export function getLeaderboard(bench, version) {
  return book(bench, version)?.leaderboard || { version, rows: [] };
}

export function getTasks(bench, version) {
  return book(bench, version)?.tasks || { version, tasks: [] };
}

export function getTask(bench, version, taskId) {
  return getTasks(bench, version).tasks.find((item) => item.task_id === taskId) || null;
}

export function getAbout(bench, version) {
  return book(bench, version)?.about || "";
}

export function getRun(bench, version, runId) {
  return book(bench, version)?.runs?.[runId] || null;
}

// Pass@5 board: five attempts per task, best attempt counts. Only RCB has one.
export function getPass5(bench, version) {
  return book(bench, version)?.pass5 || null;
}

export function getAtlas(bench, version) {
  return book(bench, version)?.atlas || null;
}

// Domain colours and short titles for a bench's tasks: RCB keeps them in atlas.json,
// AFE ships them inside tasks.json.
export function getTaskMeta(bench, version) {
  const atlas = getAtlas(bench, version);
  const pack = getTasks(bench, version);
  const domains = atlas?.domains || pack.domains || [];
  const labels = atlas?.labels || Object.fromEntries(pack.tasks.filter((t) => t.label).map((t) => [t.task_id, t.label]));
  return { domains, labels };
}

export function getSiteAbout() {
  return siteAbout;
}

export function getFields() {
  return fieldsDoc;
}

export function getCommittee() {
  return committeeDoc;
}
