<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Reports" />

    <div class="premium-hero mb-4">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
        <div>
          <div class="premium-badge mb-2">HR Modules</div>
          <h4 class="mb-1 premium-title">Reports</h4>
          <p class="mb-0 premium-subtitle">Build attendance, payroll, leave, and masterlist exports with a cleaner preview workflow.</p>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-12">
        <div class="card border-0 shadow-sm premium-panel">
          <div class="card-header d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-3 bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div>
              <h5 class="mb-0">Report Builder</h5>
              <small class="text-muted">Configure filters, preview the data, then export your report.</small>
            </div>
            <div class="d-flex flex-wrap gap-2">
              <span class="badge" :class="reportStatusBadge.class">{{ reportStatusBadge.label }}</span>
              <span class="badge bg-light-secondary text-secondary">{{ filteredRows.length }} row(s)</span>
              <span class="badge bg-light-primary text-primary">{{ currentDefinition.label }}</span>
            </div>
          </div>
          <div class="card-body premium-panel-body">
            <form novalidate @submit.prevent="generateReport">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="reportType">Report Type</label>
                  <select id="reportType" v-model="form.reportType" class="form-select premium-input" required>
                    <option value="attendance">Attendance Report</option>
                    <option value="lateUndertime">Late/Undertime Report</option>
                    <option value="employee">Employee Masterlist</option>
                    <option value="leave">Leave Report</option>
                    <option value="payroll">Payroll Report</option>
                    <option value="government">Government Contribution Report</option>
                  </select>
                </div>
                <div v-if="showDateRange" class="col-md-4 mb-3">
                  <label class="form-label" for="dateFrom">Date Range Start</label>
                  <input id="dateFrom" v-model="form.dateFrom" type="date" class="form-control premium-input" :class="fieldClass('dateFrom')" @input="handleFormMutation('dateFrom')">
                  <div class="invalid-feedback">{{ validationErrors.dateFrom }}</div>
                </div>
                <div v-if="showDateRange" class="col-md-4 mb-3">
                  <label class="form-label" for="dateTo">Date Range End</label>
                  <input id="dateTo" v-model="form.dateTo" type="date" class="form-control premium-input" :class="fieldClass('dateTo')" @input="handleFormMutation('dateTo')">
                  <div class="invalid-feedback">{{ validationErrors.dateTo }}</div>
                </div>
                <div v-if="showDateRange" class="col-md-4 mb-3 d-flex align-items-end">
                  <div class="d-flex flex-wrap gap-2 w-100">
                    <button type="button" class="btn btn-light-primary" @click="setDatePreset('today')">Today</button>
                    <button type="button" class="btn btn-light-primary" @click="setDatePreset('week')">This Week</button>
                    <button type="button" class="btn btn-light-primary" @click="setDatePreset('month')">This Month</button>
                  </div>
                </div>

                <div v-if="showDepartmentField" class="col-md-4 mb-3">
                  <label class="form-label" for="department">Department</label>
                  <input id="department" v-model="form.department" type="text" class="form-control premium-input" placeholder="Optional">
                </div>

                <div v-if="showBranchField" class="col-md-4 mb-3">
                  <label class="form-label" for="branch">Branch</label>
                  <input id="branch" v-model="form.branch" type="text" class="form-control premium-input" placeholder="Optional">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="exportTarget">Export Target</label>
                  <select id="exportTarget" v-model="form.exportTarget" class="form-select premium-input" required>
                    <option value="xlsx">Excel (.xlsx)</option>
                    <option value="csv">CSV (.csv)</option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="previewMode">Preview Mode</label>
                  <select id="previewMode" v-model="form.previewMode" class="form-select premium-input">
                    <option value="standard">Standard</option>
                    <option value="compact">Compact</option>
                  </select>
                </div>
              </div>

              <div class="d-grid gap-2 d-md-flex flex-md-wrap mt-2">
                <button type="button" class="btn btn-outline-primary premium-action" @click="refreshPreview">Preview</button>
                <button type="button" class="btn btn-outline-success premium-action" @click="exportCurrent">Export</button>
                <button type="submit" class="btn btn-primary">Generate</button>
              </div>

              <div class="alert mt-3 mb-0" :class="reportAlert.class" role="alert">
                {{ reportAlert.message }}
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-12">
        <div class="card mt-3 border-0 shadow-sm premium-panel">
          <div class="card-header d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-3 bg-white border-bottom-0 pt-4 pb-0 premium-panel-header">
            <div>
              <h5 class="mb-0">Preview Grid</h5>
              <small class="text-muted">See the filtered results before downloading.</small>
            </div>
            <span class="text-muted small">{{ filterSummary }}</span>
          </div>
          <div class="card-body premium-panel-body">
            <div class="d-none d-md-block table-responsive">
              <table class="table table-hover align-middle mb-0 premium-table">
                <thead :class="form.previewMode === 'compact' ? 'table-light' : ''">
                  <tr>
                    <th v-for="column in currentColumns" :key="column">{{ column }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, rowIndex) in filteredRows" :key="`${reportId}-${rowIndex}`">
                    <td v-for="(cell, cellIndex) in row" :key="`${rowIndex}-${cellIndex}`">{{ cell }}</td>
                  </tr>
                  <tr v-if="!filteredRows.length">
                    <td :colspan="currentColumns.length" class="text-center text-muted py-4">
                      <div class="fw-semibold mb-1">No rows found</div>
                      <div class="small">Try widening the date range or clearing filters, then preview again.</div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="d-md-none">
              <div class="premium-mobile-grid">
                <div
                  v-for="(row, rowIndex) in filteredRows"
                  :key="`mobile-row-${rowIndex}`"
                  class="border shadow-sm premium-mobile-card"
                >
                  <div class="premium-mobile-card-header">
                    <div class="premium-mobile-card-heading">
                      <div class="fw-semibold premium-mobile-card-title">{{ currentDefinition.label }}</div>
                      <div class="premium-mobile-card-subtitle">{{ mobileCardPrimaryValue(row) }}</div>
                    </div>
                  </div>

                  <div class="premium-mobile-card-actions">
                    <button
                      type="button"
                      class="btn btn-sm btn-primary premium-mobile-view-btn"
                      @click="toggleMobileRow(rowIndex)"
                    >
                      {{ isMobileRowExpanded(rowIndex) ? "Hide details" : "View details" }}
                    </button>
                  </div>

                  <div class="premium-mobile-summary">
                    <div
                      v-for="({ label, value }, summaryIndex) in getMobileSummaryEntries(row)"
                      :key="`mobile-summary-${rowIndex}-${summaryIndex}`"
                      class="premium-mobile-summary-item"
                    >
                      <span class="premium-mobile-summary-label">{{ label }}</span>
                      <span class="premium-mobile-summary-value">{{ value }}</span>
                    </div>
                  </div>

                  <div v-if="isMobileRowExpanded(rowIndex)" class="premium-mobile-row">
                    <div
                      v-for="(cell, cellIndex) in row"
                      :key="`mobile-${rowIndex}-${cellIndex}`"
                      class="premium-mobile-cell-row py-2 border-bottom"
                    >
                      <span class="text-muted small premium-mobile-cell-label">
                        {{ currentColumns[cellIndex] }}
                      </span>
                      <span class="small text-end premium-mobile-cell-value">
                        {{ cell }}
                      </span>
                    </div>
                  </div>
                </div>

                <div v-if="!filteredRows.length" class="text-center text-muted py-4">
                  <div class="fw-semibold mb-1">No rows found</div>
                  <div class="small">Try widening the date range or clearing filters, then preview again.</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";
import JSZip from "jszip";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const reportDefinitions = {
  attendance: {
    label: "Attendance Report",
    columns: ["Date", "Employee", "Late", "Undertime", "Overtime", "Night Diff", "Department"],
    rows: [],
  },
  lateUndertime: {
    label: "Late/Undertime Report",
    columns: ["Date", "Employee", "Late", "Undertime", "Department", "Branch"],
    rows: [],
  },
  employee: {
    label: "Employee Masterlist",
    columns: ["Employee ID", "Employee Name", "Department", "Branch", "Status", "Personal Email"],
    rows: [],
  },
  payroll: {
    label: "Payroll Report",
    columns: ["Payroll Run", "Employee", "Gross Pay", "Deductions", "Net Pay", "Payslip Status"],
    rows: [],
  },
  leave: {
    label: "Leave Report",
    columns: ["Employee", "Leave Type", "Start Date", "End Date", "Status", "Credits Used"],
    rows: [],
  },
  government: {
    label: "Government Contribution Report",
    columns: ["Employee", "SSS", "PhilHealth", "Pag-IBIG", "Withholding Tax", "Payroll Period"],
    rows: [],
  },
};

const form = reactive({
  reportType: "attendance",
  dateFrom: "",
  dateTo: "",
  department: "",
  branch: "",
  exportTarget: "xlsx",
  previewMode: "standard",
});

const reportAlert = reactive({
  class: "alert-light-primary border-primary",
  message: "Select a report type, apply filters, and generate a preview before exporting.",
});
const validationErrors = reactive({});

const reportId = ref(generateReportId());
const reportStatus = ref("Draft");
const backendReport = ref({
  reportType: "",
  columns: [],
  rows: [],
});
const expandedMobileRows = ref({});

function generateReportId() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const randomPart = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `RPT-${year}${month}${day}-${randomPart}`;
}

function setAlert(type, message) {
  reportAlert.class = `alert-light-${type} border-${type}`;
  reportAlert.message = message;
}

function clearValidationErrors() {
  Object.keys(validationErrors).forEach((key) => {
    delete validationErrors[key];
  });
}

function clearFieldError(fieldName) {
  if (fieldName && validationErrors[fieldName]) {
    delete validationErrors[fieldName];
  }
}

function fieldClass(fieldName) {
  return validationErrors[fieldName] ? "is-invalid" : "";
}

function handleFormMutation(fieldName = "") {
  clearFieldError(fieldName);
}

function setDatePreset(preset) {
  const now = new Date();
  const start = new Date(now);
  const end = new Date(now);

  if (preset === "week") {
    const day = now.getDay();
    const diff = day === 0 ? -6 : 1 - day;
    start.setDate(now.getDate() + diff);
    end.setDate(start.getDate() + 6);
  } else if (preset === "month") {
    start.setDate(1);
    end.setMonth(now.getMonth() + 1, 0);
  }

  form.dateFrom = start.toISOString().slice(0, 10);
  form.dateTo = end.toISOString().slice(0, 10);
  handleFormMutation("dateFrom");
  handleFormMutation("dateTo");
}

function validateForm() {
  clearValidationErrors();

  if (form.dateFrom && form.dateTo && new Date(form.dateTo) < new Date(form.dateFrom)) {
    validationErrors.dateTo = "Date range end cannot be earlier than start.";
  }

  if (Object.keys(validationErrors).length) {
    setAlert("danger", "Please complete the highlighted required fields. Optional blank fields can be skipped.");
    return false;
  }

  return true;
}

function updateStatus(label, type) {
  reportStatus.value = label;
  reportStatusBadge.value = {
    label,
    class: `bg-light-${type} text-${type}`,
  };
}

const reportStatusBadge = ref({
  label: "Draft",
  class: "bg-light-primary text-primary",
});

const currentDefinition = computed(() => reportDefinitions[form.reportType]);
const showDateRange = computed(() => ["attendance", "lateUndertime", "leave", "government"].includes(form.reportType));
const showDepartmentField = computed(() => ["attendance", "lateUndertime", "employee"].includes(form.reportType));
const showBranchField = computed(() => ["lateUndertime", "employee"].includes(form.reportType));
const backendReportType = computed(() => {
  if (form.reportType === "lateUndertime") return "attendance";
  if (form.reportType === "government") return "payroll";
  return form.reportType;
});
const hasBackendRowsForCurrentReport = computed(
  () => backendReport.value.reportType === form.reportType && backendReport.value.rows.length > 0
);
const currentColumns = computed(() =>
  hasBackendRowsForCurrentReport.value ? backendReport.value.columns : currentDefinition.value.columns
);
const filterSummary = computed(() => {
  const parts = [];

  if (form.dateFrom || form.dateTo) {
    parts.push(`${form.dateFrom || "Start"} to ${form.dateTo || "End"}`);
  }

  if (form.department.trim()) {
    parts.push(`Dept: ${form.department.trim()}`);
  }

  if (form.branch.trim()) {
    parts.push(`Branch: ${form.branch.trim()}`);
  }

  return parts.length ? parts.join(" | ") : "No filters applied";
});

function matchesFilter(row, definition) {
  const scopeDepartment = form.department.trim().toLowerCase();
  const scopeBranch = form.branch.trim().toLowerCase();
  const from = form.dateFrom ? new Date(form.dateFrom) : null;
  const to = form.dateTo ? new Date(form.dateTo) : null;

  if (definition === reportDefinitions.attendance) {
    const rowDate = new Date(row[0]);
    const rowDepartment = row[6].toLowerCase();
    if (from && rowDate < from) return false;
    if (to && rowDate > to) return false;
    if (scopeDepartment && !rowDepartment.includes(scopeDepartment)) return false;
    return true;
  }

  if (definition === reportDefinitions.employee) {
    const rowDepartment = row[2].toLowerCase();
    const rowBranch = row[3].toLowerCase();
    if (scopeDepartment && !rowDepartment.includes(scopeDepartment)) return false;
    if (scopeBranch && !rowBranch.includes(scopeBranch)) return false;
    return true;
  }

  if (definition === reportDefinitions.lateUndertime) {
    const rowDate = new Date(row[0]);
    const rowDepartment = row[4].toLowerCase();
    const rowBranch = row[5].toLowerCase();
    if (from && rowDate < from) return false;
    if (to && rowDate > to) return false;
    if (scopeDepartment && !rowDepartment.includes(scopeDepartment)) return false;
    if (scopeBranch && !rowBranch.includes(scopeBranch)) return false;
    return true;
  }

  if (definition === reportDefinitions.payroll) {
    const rowDate = new Date("2026-06-01");
    if (from && rowDate < from) return false;
    if (to && rowDate > to) return false;
    return true;
  }

  if (definition === reportDefinitions.leave) {
    const rowDate = new Date(row[2]);
    if (from && rowDate < from) return false;
    if (to && rowDate > to) return false;
    return true;
  }

  if (definition === reportDefinitions.government) {
    const rowPayrollPeriod = row[5];
    if (from || to) {
      const periodDate = new Date(`${rowPayrollPeriod}-01`);
      if (from && periodDate < from) return false;
      if (to && periodDate > to) return false;
    }
    return true;
  }

  return true;
}

const filteredRows = computed(() =>
  hasBackendRowsForCurrentReport.value
    ? backendReport.value.rows
    : currentDefinition.value.rows.filter((row) => matchesFilter(row, currentDefinition.value))
);

function mobileCardPrimaryValue(row) {
  const priorityColumns = ["Employee", "Employee Name", "Employee Code", "Log Id", "Payroll Run", "Leave Type"];

  for (const columnName of priorityColumns) {
    const index = currentColumns.value.indexOf(columnName);
    if (index >= 0 && row[index]) {
      return String(row[index]);
    }
  }

  return row.find((cell) => String(cell || "").trim()) || "Preview details";
}

function getMobileSummaryEntries(row) {
  const preferredColumns = ["Log Id", "Employee Code", "Employee", "Employee Name", "Work Date", "Date", "Status"];
  const seenColumns = new Set();
  const entries = [];

  preferredColumns.forEach((columnName) => {
    const index = currentColumns.value.indexOf(columnName);
    if (index >= 0 && row[index] !== undefined && !seenColumns.has(columnName) && entries.length < 3) {
      entries.push({
        label: columnName,
        value: String(row[index] ?? "--"),
      });
      seenColumns.add(columnName);
    }
  });

  currentColumns.value.forEach((columnName, index) => {
    if (entries.length >= 3 || seenColumns.has(columnName)) return;
    entries.push({
      label: columnName,
      value: String(row[index] ?? "--"),
    });
  });

  return entries;
}

function isMobileRowExpanded(rowIndex) {
  return Boolean(expandedMobileRows.value[rowIndex]);
}

function toggleMobileRow(rowIndex) {
  expandedMobileRows.value = {
    ...expandedMobileRows.value,
    [rowIndex]: !expandedMobileRows.value[rowIndex],
  };
}

function formatBackendColumn(column) {
  return column
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

async function loadBackendReportRows() {
  if (!authStore.accessToken) return false;

  try {
    const response = await apiRequest(`/reports/data?report_type=${encodeURIComponent(backendReportType.value)}`, {
      token: authStore.accessToken,
    });
    const rows = response.rows || [];
    const keys = rows.length ? Object.keys(rows[0]) : [];
    backendReport.value = {
      reportType: form.reportType,
      columns: keys.length ? keys.map(formatBackendColumn) : currentDefinition.value.columns,
      rows: rows.map((row) => keys.map((key) => row[key] ?? "")),
    };
    return true;
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      authStore.logout();
    }
    backendReport.value = { reportType: "", columns: [], rows: [] };
    return false;
  }
}

async function refreshPreview() {
  if (!validateForm()) return;
  const usedBackendData = await loadBackendReportRows();
  updateStatus("Generated", "success");
  setAlert(
    "success",
    `${currentDefinition.value.label} preview generated with ${filteredRows.value.length} row(s)${usedBackendData ? " from the HRIS API" : ""}.`
  );
}

function downloadBlob(blob, fileName) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function exportCsv() {
  const lines = [currentColumns.value.join(",")].concat(
    filteredRows.value.map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(","))
  );
  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
  downloadBlob(blob, `${form.reportType}-report.csv`);
}

function escapeXml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

async function exportXlsx() {
  const zip = new JSZip();
  const sheetRows = [
    `<row r="1">${currentColumns.value
      .map((column, index) => `<c r="${String.fromCharCode(65 + index)}1" t="inlineStr"><is><t>${escapeXml(column)}</t></is></c>`)
      .join("")}</row>`,
  ].concat(
    filteredRows.value.map((row, rowIndex) => {
      const rowNumber = rowIndex + 2;
      return `<row r="${rowNumber}">${row
        .map((cell, cellIndex) => {
          const cellRef = `${String.fromCharCode(65 + cellIndex)}${rowNumber}`;
          return `<c r="${cellRef}" t="inlineStr"><is><t>${escapeXml(cell)}</t></is></c>`;
        })
        .join("")}</row>`;
    })
  );

  const workbookXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="${escapeXml(currentDefinition.value.label)}" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>`;
  const relsXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>`;
  const contentTypesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>`;
  const rootRelsXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>`;
  const stylesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
  <fills count="1"><fill><patternFill patternType="none"/></fill></fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>
</styleSheet>`;
  const sheetXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    ${sheetRows.join("")}
  </sheetData>
</worksheet>`;

  zip.file("[Content_Types].xml", contentTypesXml);
  zip.folder("_rels").file(".rels", rootRelsXml);
  zip.folder("xl").file("workbook.xml", workbookXml);
  zip.folder("xl").folder("_rels").file("workbook.xml.rels", relsXml);
  zip.folder("xl").file("styles.xml", stylesXml);
  zip.folder("xl").folder("worksheets").file("sheet1.xml", sheetXml);

  const blob = await zip.generateAsync({
    type: "blob",
    mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  });
  downloadBlob(blob, `${form.reportType}-report.xlsx`);
}

async function exportCurrent() {
  if (!validateForm()) return;
  await refreshPreview();
  if (form.exportTarget === "csv") {
    exportCsv();
    setAlert("success", `${currentDefinition.value.label} exported as CSV.`);
    return;
  }

  await exportXlsx();
  setAlert("success", `${currentDefinition.value.label} export started as XLSX.`);
}

async function generateReport() {
  reportId.value = generateReportId();
  if (!validateForm()) {
    updateStatus("Draft", "primary");
    return;
  }

  await loadBackendReportRows();
  updateStatus("Generated", "success");
  setAlert(
    "success",
    `${reportId.value.trim()} generated with ${filteredRows.value.length} visible row(s).`
  );
}

watch(
  () => [
    form.reportType,
    form.dateFrom,
    form.dateTo,
    form.department,
    form.branch,
    form.previewMode,
    form.exportTarget,
  ],
  () => {
    expandedMobileRows.value = {};
    refreshPreview();
  },
  { deep: true }
);

refreshPreview();
</script>

<style scoped>
.premium-hero {
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 1.5rem;
  padding: 1.25rem 1.5rem;
  background:
    linear-gradient(135deg, rgba(13, 110, 253, 0.08), rgba(13, 110, 253, 0.02)),
    #fff;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}

.premium-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  border-radius: 999px;
  padding: 0.35rem 0.75rem;
  background: rgba(13, 110, 253, 0.08);
  color: #0d6efd;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.premium-title {
  font-weight: 800;
  letter-spacing: -0.03em;
}

.premium-subtitle {
  color: #64748b;
  max-width: 56rem;
}

.premium-panel {
  border-radius: 1.35rem;
  border: 1px solid rgba(16, 24, 40, 0.06);
  overflow: hidden;
}

.premium-panel-header {
  padding-bottom: 1rem;
}

.premium-panel-body {
  background:
    radial-gradient(circle at top left, rgba(13, 110, 253, 0.05), transparent 35%),
    #fff;
}

.premium-input {
  border-color: rgba(148, 163, 184, 0.22);
}

.premium-input:focus {
  box-shadow: none;
  border-color: #0d6efd;
}

.premium-action {
  border-color: rgba(13, 110, 253, 0.22);
}

.premium-table thead th {
  color: #475569;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom-color: rgba(148, 163, 184, 0.2);
}

.premium-table tbody td {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.premium-mobile-card {
  display: block;
  width: 100%;
  max-width: 100%;
  min-width: 0;
  margin: 0;
  padding: 1rem;
  border-radius: 0;
  box-sizing: border-box;
  overflow: hidden;
  align-self: stretch;
  border-color: rgba(148, 163, 184, 0.18) !important;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
}

.premium-mobile-card-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.premium-mobile-card-heading {
  min-width: 0;
  flex: 1 1 auto;
}

.premium-mobile-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  min-width: 0;
  margin-top: 1.25rem;
}

.premium-mobile-card-title {
  line-height: 1.2;
  word-break: break-word;
}

.premium-mobile-card-subtitle {
  margin-top: 0.3rem;
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.35;
  word-break: break-word;
}

.premium-mobile-card-actions {
  margin: 0.9rem 0 0.95rem;
}

.premium-mobile-view-btn {
  flex-shrink: 0;
  border-radius: 999px;
  padding: 0.55rem 1rem;
  font-weight: 600;
}

.premium-mobile-summary {
  display: grid;
  gap: 0.55rem;
  margin-bottom: 0.75rem;
  min-width: 0;
}

.premium-mobile-summary-item {
  display: flex;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.65rem 0.8rem;
  border-radius: 0.9rem;
  background: rgba(248, 250, 252, 0.95);
  border: 1px solid rgba(148, 163, 184, 0.16);
}

.premium-mobile-summary-label {
  min-width: 0;
  color: #64748b;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.premium-mobile-summary-value {
  min-width: 0;
  flex: 1 1 auto;
  color: #0f172a;
  font-size: 0.88rem;
  font-weight: 600;
  text-align: right;
  word-break: break-word;
  overflow-wrap: anywhere;
}

.premium-mobile-row {
  min-width: 0;
  padding-top: 0.25rem;
  border-top: 1px solid rgba(148, 163, 184, 0.18);
}

.premium-mobile-cell-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr);
  align-items: start;
  column-gap: 0.85rem;
  min-width: 0;
}

.premium-mobile-cell-label {
  min-width: 0;
  word-break: break-word;
  overflow-wrap: anywhere;
  line-height: 1.3;
}

.premium-mobile-cell-value {
  min-width: 0;
  word-break: break-word;
  overflow-wrap: anywhere;
  line-height: 1.3;
  text-align: right;
}

.premium-mobile-row .premium-mobile-cell-row:last-child {
  border-bottom: 0 !important;
}

@media (max-width: 767.98px) {
  .premium-mobile-grid {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .premium-mobile-card {
    width: 100%;
    max-width: 100%;
    margin: 0;
    padding: 14px;
  }

  .premium-mobile-grid,
  .premium-mobile-card-header,
  .premium-mobile-summary-item {
    flex-direction: column;
    align-items: stretch;
  }

  .premium-mobile-view-btn {
    width: 100%;
  }

  .premium-mobile-summary-value {
    text-align: left;
  }

  .premium-mobile-cell-row {
    grid-template-columns: minmax(0, 1fr);
    row-gap: 0.25rem;
  }

  .premium-mobile-cell-value {
    text-align: left;
  }

  .premium-hero {
    padding: 1rem 1.1rem;
    border-radius: 1.15rem;
  }

  .premium-panel-header {
    padding-top: 1.1rem !important;
  }
}
</style>
