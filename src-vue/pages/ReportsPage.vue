<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Reports" />

    <div class="row g-3">
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex align-items-center justify-content-between">
            <h5 class="mb-0">Report Builder</h5>
            <span class="badge" :class="reportStatusBadge.class">{{ reportStatusBadge.label }}</span>
          </div>
          <div class="card-body">
            <form novalidate @submit.prevent="generateReport">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="reportType">Report Type</label>
                  <select id="reportType" v-model="form.reportType" class="form-select" required>
                    <option value="attendance">Attendance Report</option>
                    <option value="lateUndertime">Late/Undertime Report</option>
                    <option value="employee">Employee Masterlist</option>
                    <option value="leave">Leave Report</option>
                    <option value="payroll">Payroll Report</option>
                    <option value="government">Government Contribution Report</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="operatorId">Authorized Operator ID</label>
                  <input id="operatorId" v-model="form.operatorId" type="text" class="form-control" :class="fieldClass('operatorId')" placeholder="HR-ADMIN-01" required @input="handleFormMutation('operatorId')">
                  <div class="invalid-feedback">{{ validationErrors.operatorId }}</div>
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="dateFrom">Date Range Start</label>
                  <input id="dateFrom" v-model="form.dateFrom" type="date" class="form-control" :class="fieldClass('dateFrom')" @input="handleFormMutation('dateFrom')">
                  <div class="invalid-feedback">{{ validationErrors.dateFrom }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="dateTo">Date Range End</label>
                  <input id="dateTo" v-model="form.dateTo" type="date" class="form-control" :class="fieldClass('dateTo')" @input="handleFormMutation('dateTo')">
                  <div class="invalid-feedback">{{ validationErrors.dateTo }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="department">Department</label>
                  <input id="department" v-model="form.department" type="text" class="form-control" placeholder="Optional">
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="branch">Branch</label>
                  <input id="branch" v-model="form.branch" type="text" class="form-control" placeholder="Optional">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="exportTarget">Export Target</label>
                  <select id="exportTarget" v-model="form.exportTarget" class="form-select" required>
                    <option value="xlsx">Excel (.xlsx)</option>
                    <option value="csv">CSV (.csv)</option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="previewMode">Preview Mode</label>
                  <select id="previewMode" v-model="form.previewMode" class="form-select">
                    <option value="standard">Standard</option>
                    <option value="compact">Compact</option>
                  </select>
                </div>
              </div>

              <div class="d-flex flex-wrap gap-2 mt-2">
                <button type="button" class="btn btn-outline-primary" @click="refreshPreview">Refresh Preview</button>
                <button type="button" class="btn btn-outline-success" @click="exportCurrent">Export Report</button>
                <button type="submit" class="btn btn-primary">Generate Report</button>
              </div>

              <div class="alert mt-3 mb-0" :class="reportAlert.class" role="alert">
                {{ reportAlert.message }}
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-12">
        <div class="card mt-3">
          <div class="card-header d-flex align-items-center justify-content-between">
            <h5 class="mb-0">Preview Grid</h5>
            <span class="text-muted small">Dynamic columns based on report selection</span>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover table-bordered align-middle mb-0">
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
                      No rows match the selected report scope.
                    </td>
                  </tr>
                </tbody>
              </table>
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
  operatorId: "",
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

function validateForm({ requireOperator = true } = {}) {
  clearValidationErrors();

  if (requireOperator && !form.operatorId.trim()) {
    validationErrors.operatorId = "Authorized Operator ID is required.";
  }

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
  if (!validateForm({ requireOperator: false })) return;
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
    `${reportId.value.trim()} generated by ${form.operatorId.trim()} with ${filteredRows.value.length} visible row(s).`
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
    refreshPreview();
  },
  { deep: true }
);

refreshPreview();
</script>
