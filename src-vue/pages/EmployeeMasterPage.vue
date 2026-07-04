<template>
  <div>
    <BreadcrumbBar section="HR Modules" current="Employee Master" />

    <div class="row g-3">
      <div class="col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Total Employees</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ isDirectoryLoading ? "..." : overview.totalEmployees }}</h3>
                <span class="text-muted small">Profiles in directory</span>
              </div>
              <span class="badge bg-light-primary text-primary">Masterlist</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Active Access</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ isDirectoryLoading ? "..." : overview.activeAccounts }}</h3>
                <span class="text-muted small">Employees with HRIS access</span>
              </div>
              <span class="badge bg-light-success text-success">Access</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">In Onboarding</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ isDirectoryLoading ? "..." : overview.onboardingEmployees }}</h3>
                <span class="text-muted small">Employees not yet completed</span>
              </div>
              <span class="badge bg-light-warning text-warning">Lifecycle</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <small class="text-muted d-block mb-2">Missing Documents</small>
            <div class="d-flex align-items-end justify-content-between">
              <div>
                <h3 class="mb-1">{{ isDirectoryLoading ? "..." : overview.missingDocuments }}</h3>
                <span class="text-muted small">Records with incomplete files</span>
              </div>
              <span class="badge bg-light-danger text-danger">Compliance</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-8">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <div>
              <h5 class="mb-0">Employee Profile</h5>
              <small class="text-muted">Create and maintain the core employee record used by all other HR modules.</small>
            </div>
            <span class="badge" :class="profileBadge.class">{{ profileBadge.label }}</span>
          </div>
          <div class="card-body">
            <form novalidate @submit.prevent="handleSubmit">
              <div class="d-flex align-items-center justify-content-between mb-3">
                <div>
                  <h6 class="mb-1">1. Basic profile</h6>
                  <p class="text-muted mb-0 small">Capture identity, hiring, and access-related details first.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="employeeId">Employee ID</label>
                  <input id="employeeId" v-model="form.employeeId" type="text" class="form-control" :class="fieldClass('employeeId')" placeholder="Auto-generated" readonly>
                  <div class="invalid-feedback">{{ validationErrors.employeeId }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="dateHired">Date Hired</label>
                  <input id="dateHired" v-model="form.dateHired" type="date" class="form-control" :class="fieldClass('dateHired')" @input="handleFormMutation('dateHired')">
                  <div class="invalid-feedback">{{ validationErrors.dateHired }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="employmentStatus">Employment Status</label>
                  <select id="employmentStatus" v-model="form.employmentStatus" class="form-select" :class="fieldClass('employmentStatus')" @change="handleFormMutation('employmentStatus')">
                    <option value="">Select status</option>
                    <option>Probationary</option>
                    <option>Regular</option>
                    <option>Contractual</option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.employmentStatus }}</div>
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="firstName">First Name</label>
                  <input id="firstName" v-model="form.firstName" type="text" class="form-control" :class="fieldClass('firstName')" @input="handleFormMutation('firstName')">
                  <div class="invalid-feedback">{{ validationErrors.firstName }}</div>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="middleName">Middle Name</label>
                  <input id="middleName" v-model="form.middleName" type="text" class="form-control" @input="handleFormMutation">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="lastName">Last Name</label>
                  <input id="lastName" v-model="form.lastName" type="text" class="form-control" :class="fieldClass('lastName')" @input="handleFormMutation('lastName')">
                  <div class="invalid-feedback">{{ validationErrors.lastName }}</div>
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label" for="personalEmail">Personal Email</label>
                  <input id="personalEmail" v-model="form.personalEmail" type="email" class="form-control" :class="fieldClass('personalEmail')" placeholder="name@email.com" @input="handleFormMutation('personalEmail')">
                  <div class="invalid-feedback">{{ validationErrors.personalEmail }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="contactNumber">Contact Number</label>
                  <input id="contactNumber" v-model="form.contactNumber" type="text" class="form-control" placeholder="0917-123-4567" @input="handleFormMutation">
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="birthDate">Birth Date</label>
                  <input id="birthDate" v-model="form.birthDate" type="date" class="form-control" @input="handleFormMutation">
                </div>

                <div class="col-md-8 mb-3">
                  <label class="form-label" for="address">Address</label>
                  <input id="address" v-model="form.address" type="text" class="form-control" placeholder="City, province, and street address" @input="handleFormMutation">
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="accountStatus">Account Status</label>
                  <select id="accountStatus" v-model="form.accountStatus" class="form-select" @change="handleFormMutation">
                    <option>Active</option>
                    <option>Inactive</option>
                    <option>Separated</option>
                  </select>
                </div>
              </div>

              <div class="d-flex align-items-center justify-content-between mt-2 mb-3">
                <div>
                  <h6 class="mb-1">2. Employment details</h6>
                  <p class="text-muted mb-0 small">Use controlled fields to keep department, position, branch, and manager records consistent.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="department">Department</label>
                  <select id="department" v-model="form.department" class="form-select" :class="fieldClass('department')" @change="handleDepartmentChange">
                    <option value="">Select department</option>
                    <option v-for="department in departmentOptions" :key="department">{{ department }}</option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.department }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="position">Position</label>
                  <select id="position" v-model="form.position" class="form-select" :class="fieldClass('position')" :disabled="!form.department" @change="handlePositionChange">
                    <option value="">Select position</option>
                    <option v-for="position in selectedPositionOptions" :key="position">{{ position }}</option>
                    <option value="__custom">Other / Custom</option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.position }}</div>
                </div>
                <div v-if="isCustomPosition" class="col-md-3 mb-3">
                  <label class="form-label" for="customPosition">Custom Position</label>
                  <input id="customPosition" v-model="form.customPosition" type="text" class="form-control" :class="fieldClass('customPosition')" placeholder="Enter position title" @input="handleFormMutation('customPosition')">
                  <div class="invalid-feedback">{{ validationErrors.customPosition }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="branch">Branch</label>
                  <select id="branch" v-model="form.branch" class="form-select" :class="fieldClass('branch')" @change="handleFormMutation('branch')">
                    <option value="">Select branch</option>
                    <option>Main Branch</option>
                    <option>Quezon Branch</option>
                    <option>Cebu Branch</option>
                    <option>Davao Branch</option>
                  </select>
                  <div class="invalid-feedback">{{ validationErrors.branch }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="manager">Immediate Supervisor</label>
                  <select id="manager" v-model="form.manager" class="form-select" @change="handleFormMutation">
                    <option value="">Select manager</option>
                    <option v-for="manager in managerOptions" :key="manager.id" :value="manager.name">{{ manager.name }}</option>
                  </select>
                </div>
              </div>

              <div class="d-flex align-items-center justify-content-between mt-2 mb-3">
                <div>
                  <h6 class="mb-1">3. Lifecycle and movement</h6>
                  <p class="text-muted mb-0 small">Show onboarding by default, and reveal offboarding only for separated or resigned employees.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="onboardingStage">Onboarding Stage</label>
                  <select id="onboardingStage" v-model="form.onboardingStage" class="form-select" @change="handleFormMutation">
                    <option>Pre-boarding</option>
                    <option>Onboarding</option>
                    <option>Completed</option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="movementType">Movement Type</label>
                  <select id="movementType" v-model="form.movementType" class="form-select" @change="handleFormMutation">
                    <option>None</option>
                    <option>Promotion</option>
                    <option>Transfer</option>
                    <option>Resignation</option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label" for="movementEffectiveDate">Movement Effective Date</label>
                  <input id="movementEffectiveDate" v-model="form.movementEffectiveDate" type="date" class="form-control" @input="handleFormMutation">
                </div>
                <div class="col-md-12 mb-3">
                  <label class="form-label" for="movementRemarks">Movement Remarks</label>
                  <input id="movementRemarks" v-model="form.movementRemarks" type="text" class="form-control" placeholder="Promotion, transfer, or resignation note" @input="handleFormMutation">
                </div>
              </div>

              <div v-if="showOffboardingPanel" class="border rounded p-3 mb-3">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div>
                    <h6 class="mb-1">Offboarding details</h6>
                    <p class="text-muted mb-0 small">Required only when the employee is separated or has a resignation movement.</p>
                  </div>
                  <span class="badge bg-light-danger text-danger">Exit Process</span>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label" for="offboardingDate">Offboarding Date</label>
                    <input id="offboardingDate" v-model="form.offboardingDate" type="date" class="form-control" :class="fieldClass('offboardingDate')" @input="handleFormMutation('offboardingDate')">
                    <div class="invalid-feedback">{{ validationErrors.offboardingDate }}</div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label" for="offboardingReason">Offboarding Reason</label>
                    <select id="offboardingReason" v-model="form.offboardingReason" class="form-select" :class="fieldClass('offboardingReason')" @change="handleFormMutation('offboardingReason')">
                      <option value="">Select reason</option>
                      <option>Resignation</option>
                      <option>Transfer</option>
                      <option>Retirement</option>
                      <option>Termination</option>
                    </select>
                    <div class="invalid-feedback">{{ validationErrors.offboardingReason }}</div>
                  </div>
                </div>
              </div>

              <div class="d-flex align-items-center justify-content-between mt-2 mb-3">
                <div>
                  <h6 class="mb-1">4. Statutory, banking, and documents</h6>
                  <p class="text-muted mb-0 small">Validate government identifiers and track required file submissions.</p>
                </div>
              </div>

              <div class="row">
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="sss">SSS</label>
                  <input id="sss" v-model="form.sss" type="text" class="form-control" :class="fieldClass('sss')" placeholder="12-3456789-0" @input="handleFormMutation('sss')">
                  <div class="invalid-feedback">{{ validationErrors.sss }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="philhealth">PhilHealth</label>
                  <input id="philhealth" v-model="form.philhealth" type="text" class="form-control" :class="fieldClass('philhealth')" placeholder="12-345678901-2" @input="handleFormMutation('philhealth')">
                  <div class="invalid-feedback">{{ validationErrors.philhealth }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="pagibig">Pag-IBIG</label>
                  <input id="pagibig" v-model="form.pagibig" type="text" class="form-control" :class="fieldClass('pagibig')" placeholder="1234-5678-9012" @input="handleFormMutation('pagibig')">
                  <div class="invalid-feedback">{{ validationErrors.pagibig }}</div>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label" for="tin">TIN</label>
                  <input id="tin" v-model="form.tin" type="text" class="form-control" :class="fieldClass('tin')" placeholder="123-456-789-000" @input="handleFormMutation('tin')">
                  <div class="invalid-feedback">{{ validationErrors.tin }}</div>
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label" for="bankAccount">Bank Account Details</label>
                  <input id="bankAccount" v-model="form.bankAccount" type="text" class="form-control" :class="fieldClass('bankAccount')" placeholder="Bank name and account number" @input="handleFormMutation('bankAccount')">
                  <div class="invalid-feedback">{{ validationErrors.bankAccount }}</div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="emergencyContact">Emergency Contact</label>
                  <input id="emergencyContact" v-model="form.emergencyContact" type="text" class="form-control" placeholder="Name and contact number" @input="handleFormMutation">
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label d-block">Document Checklist</label>
                  <div class="form-check mb-2">
                    <input id="docContract" v-model="form.documents.contract" class="form-check-input" type="checkbox" @change="handleFormMutation">
                    <label class="form-check-label" for="docContract">Employment Contract</label>
                  </div>
                  <div class="form-check mb-2">
                    <input id="docGovIds" v-model="form.documents.govIds" class="form-check-input" type="checkbox" @change="handleFormMutation">
                    <label class="form-check-label" for="docGovIds">Government IDs</label>
                  </div>
                  <div class="form-check mb-2">
                    <input id="docBankForm" v-model="form.documents.bankForm" class="form-check-input" type="checkbox" @change="handleFormMutation">
                    <label class="form-check-label" for="docBankForm">Bank Enrollment Form</label>
                  </div>
                  <div class="form-check">
                    <input id="docClearance" v-model="form.documents.clearance" class="form-check-input" type="checkbox" @change="handleFormMutation">
                    <label class="form-check-label" for="docClearance">Clearance / Exit Documents</label>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label" for="documentUpload">Document Management</label>
                  <input id="documentUpload" type="file" class="form-control" multiple @change="handleDocumentUpload">
                  <small class="text-muted">Upload contracts, IDs, forms, or clearance files.</small>
                </div>

                <div class="col-md-12 mb-3">
                  <label class="form-label" for="notes">Notes</label>
                  <input id="notes" v-model="form.notes" type="text" class="form-control" placeholder="Optional audit or HR notes" @input="handleFormMutation">
                </div>
              </div>

              <div class="d-flex flex-wrap gap-2 mt-2">
                <button type="button" class="btn btn-outline-secondary" @click="startNewEmployee">New Employee</button>
                <button type="button" class="btn btn-outline-primary" @click="saveDraft">Save Draft</button>
                <button type="submit" class="btn btn-primary" :disabled="isSubmitting">{{ submitButtonLabel }}</button>
              </div>

              <div class="alert mt-3 mb-0" :class="alertState.class" role="alert">
                {{ alertState.message }}
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-header bg-light-primary border-0">
            <h5 class="mb-0 text-primary">Profile Summary</h5>
            <small class="text-muted">Read-only preview of the employee record.</small>
          </div>
          <div class="card-body">
            <div class="mb-3 p-3 rounded bg-light">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Account Access</span>
                <span class="badge" :class="accessPreview.class">{{ accessPreview.label }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Employee</span>
                <strong>{{ employeeSummary }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Assignment</span>
                <strong>{{ assignmentSummary }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-muted">Manager</span>
                <strong>{{ managerSummary }}</strong>
              </div>
            </div>

            <div class="row g-3">
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Onboarding</small>
                  <h5 class="mb-0">{{ onboardingSummary }}</h5>
                </div>
              </div>
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Movement</small>
                  <h5 class="mb-0">{{ movementSummary }}</h5>
                </div>
              </div>
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Employment</small>
                  <h5 class="mb-0">{{ employmentSummary }}</h5>
                </div>
              </div>
              <div class="col-6">
                <div class="border rounded p-3 h-100">
                  <small class="text-muted d-block mb-1">Documents</small>
                  <h5 class="mb-0 text-success">{{ documentSummary }}</h5>
                </div>
              </div>
            </div>

            <div class="mt-3 p-3 rounded bg-light-primary border border-primary-subtle">
              <strong class="d-block text-primary mb-1">Access rule</strong>
              <small class="text-muted d-block">Changing account status immediately updates whether the employee should have active HRIS access.</small>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-12">
        <div class="card">
          <div class="card-header d-flex flex-wrap gap-2 align-items-center justify-content-between">
            <div>
              <h5 class="mb-0">Employee Directory</h5>
              <small class="text-muted">Search, filter, and load employee records into the form.</small>
            </div>
            <div class="d-flex flex-wrap align-items-center gap-2">
              <input v-model="employeeSearch" type="search" class="form-control" placeholder="Search employee" style="min-width: 220px;">
              <span class="badge bg-light-secondary text-secondary">{{ employeeCountLabel }}</span>
            </div>
          </div>
          <div class="card-body p-0">
            <div class="px-3 pt-3 d-flex flex-wrap gap-2">
              <button
                v-for="filter in directoryFilters"
                :key="filter.value"
                type="button"
                class="btn btn-sm"
                :class="activeDirectoryFilter === filter.value ? 'btn-primary' : 'btn-outline-primary'"
                @click="activeDirectoryFilter = filter.value"
              >
                {{ filter.label }}
              </button>
            </div>
            <div v-if="directoryError" class="px-3 pt-3">
              <div class="alert alert-light-warning border-warning mb-0">{{ directoryError }}</div>
            </div>
            <div class="table-responsive mt-3">
              <table class="table table-hover mb-0 align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Employee ID</th>
                    <th>Name</th>
                    <th>Department / Position / Branch</th>
                    <th>Status</th>
                    <th>Lifecycle</th>
                    <th>Documents</th>
                    <th>Email</th>
                    <th class="text-end">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in filteredDirectory" :key="row.id">
                    <td>{{ row.id }}</td>
                    <td>{{ row.name }}</td>
                    <td>{{ row.assignment }}</td>
                    <td><span class="badge" :class="row.statusClass">{{ row.statusLabel }}</span></td>
                    <td><span class="badge" :class="row.lifecycleClass">{{ row.lifecycleLabel }}</span></td>
                    <td>{{ row.documentsLabel }}</td>
                    <td>{{ row.email }}</td>
                    <td class="text-end">
                      <a href="#" class="btn btn-sm btn-outline-primary" @click.prevent="loadEmployeeRecord(row.id)">View</a>
                    </td>
                  </tr>
                  <tr v-if="!filteredDirectory.length">
                    <td colspan="8" class="text-center text-muted py-4">No employee record matches the current search or filter.</td>
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
import { computed, onMounted, reactive, ref, watch } from "vue";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { ApiError, apiRequest } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const baseDirectory = ref([]);

const existingEmployeeIds = computed(() => baseDirectory.value.map((row) => row.id));
const existingEmails = computed(() => baseDirectory.value.map((row) => row.email.toLowerCase()));
const directoryError = ref("");
const isDirectoryLoading = ref(false);
const isEditingExisting = ref(false);
const isSubmitting = ref(false);

const employeeRecords = {};

const departmentOptions = ["Human Resources", "Finance", "Operations", "IT"];

const positionOptionsByDepartment = {
  "Human Resources": ["HR Assistant", "HR Officer", "HR Manager", "Recruitment Specialist", "Training Coordinator"],
  Finance: ["Accounting Staff", "Bookkeeper", "Finance Analyst", "Payroll Admin", "Finance Manager"],
  Operations: ["Operations Staff", "Operations Coordinator", "Operations Supervisor", "Branch Manager", "Attendance Clerk"],
  IT: ["IT Staff", "IT Support Specialist", "System Administrator", "Network Administrator", "IT Manager"],
};

const directoryFilters = [
  { value: "all", label: "All" },
  { value: "active", label: "Active Access" },
  { value: "probationary", label: "Probationary" },
  { value: "separated", label: "Separated" },
  { value: "missing-docs", label: "Missing Docs" },
];

const employeeSearch = ref("");
const activeDirectoryFilter = ref("all");
const profileState = ref("Draft");
const alertState = reactive({
  class: "alert-light-primary border-primary",
  message: "Fill out the profile to validate identity, employment setup, statutory data, and account access.",
});
const validationErrors = reactive({});

const form = reactive(createEmptyForm());
const loadedEmployeeId = ref("");

function createEmptyForm() {
  return {
    employeeId: "",
    dateHired: "",
    employmentStatus: "",
    firstName: "",
    middleName: "",
    lastName: "",
    personalEmail: "",
    contactNumber: "",
    birthDate: "",
    address: "",
    accountStatus: "Active",
    department: "",
    position: "",
    customPosition: "",
    branch: "",
    manager: "",
    onboardingStage: "Pre-boarding",
    movementType: "None",
    movementEffectiveDate: "",
    movementRemarks: "",
    offboardingDate: "",
    offboardingReason: "",
    sss: "",
    philhealth: "",
    pagibig: "",
    tin: "",
    bankAccount: "",
    emergencyContact: "",
    notes: "",
    documents: {
      contract: false,
      govIds: false,
      bankForm: false,
      clearance: false,
    },
    uploads: [],
  };
}

const overview = computed(() => ({
  totalEmployees: baseDirectory.value.length,
  activeAccounts: baseDirectory.value.filter((row) => row.account === "active").length,
  onboardingEmployees: baseDirectory.value.filter((row) => row.lifecycle === "onboarding").length,
  missingDocuments: baseDirectory.value.filter((row) => row.documents < 4).length,
}));

const managerOptions = computed(() =>
  baseDirectory.value
    .filter((row) => row.account === "active")
    .map((row) => ({ id: row.id, name: row.name }))
);

function generateNextEmployeeId() {
  const maxNumber = existingEmployeeIds.value.reduce((max, id) => {
    const match = /^EMP-(\d+)$/.exec(id);
    return match ? Math.max(max, Number(match[1])) : max;
  }, 0);

  return `EMP-${String(maxNumber + 1).padStart(4, "0")}`;
}

function ensureGeneratedEmployeeId() {
  if (!isEditingExisting.value && !form.employeeId) {
    form.employeeId = generateNextEmployeeId();
  }
}

function ensureUniqueGeneratedEmployeeId() {
  if (isEditingExisting.value) return;

  while (existingEmployeeIds.value.includes(form.employeeId)) {
    form.employeeId = generateNextEmployeeId();
  }
}

const showOffboardingPanel = computed(
  () => form.accountStatus === "Separated" || form.movementType === "Resignation"
);

const documentCount = computed(
  () =>
    [
      form.documents.contract,
      form.documents.govIds,
      form.documents.bankForm,
      form.documents.clearance,
    ].filter(Boolean).length
);

const employeeSummary = computed(() => {
  const name = [form.firstName.trim(), form.middleName.trim(), form.lastName.trim()]
    .filter(Boolean)
    .join(" ");
  return name || "No employee profile yet";
});

const selectedPositionOptions = computed(() => positionOptionsByDepartment[form.department] || []);
const isCustomPosition = computed(() => form.position === "__custom");
const effectivePosition = computed(() =>
  isCustomPosition.value ? form.customPosition.trim() : form.position
);

const assignmentSummary = computed(() =>
  form.department && effectivePosition.value && form.branch
    ? `${form.department} / ${effectivePosition.value} / ${form.branch}`
    : "Department / Position / Branch"
);

const managerSummary = computed(() => form.manager || "Not assigned");
const onboardingSummary = computed(() => form.onboardingStage || "Pre-boarding");
const movementSummary = computed(() =>
  form.movementType === "None"
    ? "None"
    : `${form.movementType}${form.movementEffectiveDate ? ` (${form.movementEffectiveDate})` : ""}`
);
const employmentSummary = computed(() => form.employmentStatus || "-");
const documentSummary = computed(() => `${documentCount.value} / 4`);

const accessPreview = computed(() => {
  if (form.accountStatus === "Active") {
    return { label: "Active", class: "bg-light-success text-success" };
  }
  if (form.accountStatus === "Inactive") {
    return { label: "Restricted", class: "bg-light-warning text-warning" };
  }
  return { label: "Removed", class: "bg-light-danger text-danger" };
});

const profileBadge = computed(() => {
  const states = {
    Draft: { label: "Draft", class: "bg-light-primary text-primary" },
    Loaded: { label: "Loaded", class: "bg-light-info text-info" },
    Saved: { label: "Saved", class: "bg-light-success text-success" },
    Active: { label: "Active", class: "bg-light-success text-success" },
    Inactive: { label: "Inactive", class: "bg-light-warning text-warning" },
    Separated: { label: "Separated", class: "bg-light-danger text-danger" },
  };
  return states[profileState.value] || states.Draft;
});

const filteredDirectory = computed(() => {
  const query = employeeSearch.value.trim().toLowerCase();

  return baseDirectory.value
    .filter((row) => {
      if (activeDirectoryFilter.value === "active") return row.account === "active";
      if (activeDirectoryFilter.value === "probationary") return row.employment === "probationary";
      if (activeDirectoryFilter.value === "separated") return row.account === "separated";
      if (activeDirectoryFilter.value === "missing-docs") return row.documents < 4;
      return true;
    })
    .filter((row) => {
      if (!query) return true;
      const haystack = `${row.id} ${row.name} ${row.assignment} ${row.statusLabel} ${row.lifecycleLabel} ${row.documentsLabel} ${row.email}`.toLowerCase();
      return haystack.includes(query);
    })
    .map((row) => ({
      ...row,
      documentsLabel: `${row.documents} / 4`,
    }));
});

const employeeCountLabel = computed(() => {
  const count = filteredDirectory.value.length;
  return `${count} record${count === 1 ? "" : "s"}`;
});

const submitButtonLabel = computed(() => {
  if (isSubmitting.value) {
    return isEditingExisting.value ? "Updating..." : "Creating...";
  }
  return isEditingExisting.value ? "Update Employee Profile" : "Create Employee Profile";
});

function setAlert(type, message) {
  alertState.class = `alert-light-${type} border-${type}`;
  alertState.message = message;
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

function syncProfileStateFromAccess() {
  if (form.accountStatus === "Active") profileState.value = "Active";
  else if (form.accountStatus === "Inactive") profileState.value = "Inactive";
  else profileState.value = "Separated";
}

function handleFormMutation(fieldName = "") {
  clearFieldError(fieldName);
  syncProfileStateFromAccess();
}

function handleDepartmentChange() {
  clearFieldError("department");
  clearFieldError("position");
  clearFieldError("customPosition");
  form.position = "";
  form.customPosition = "";
  handleFormMutation();
}

function handlePositionChange() {
  clearFieldError("position");
  clearFieldError("customPosition");
  if (!isCustomPosition.value) {
    form.customPosition = "";
  }
  handleFormMutation();
}

function syncPositionSelection() {
  if (!form.position || form.position === "__custom") return;
  const isKnownPosition = (positionOptionsByDepartment[form.department] || []).includes(form.position);
  if (!isKnownPosition) {
    form.customPosition = form.position;
    form.position = "__custom";
  }
}

function handleDocumentUpload(event) {
  form.uploads = Array.from(event.target.files || []);
  handleFormMutation();
}

function validStatutory(value, pattern) {
  if (!value) return true;
  return pattern.test(value.trim());
}

function validateForm() {
  clearValidationErrors();
  ensureGeneratedEmployeeId();
  ensureUniqueGeneratedEmployeeId();

  const idValue = form.employeeId.trim();
  const emailValue = form.personalEmail.trim().toLowerCase();
  const fullName = [form.firstName, form.middleName, form.lastName].filter(Boolean).join(" ").trim();

  if (!idValue) validationErrors.employeeId = "Employee ID is required.";
  if (!form.dateHired) validationErrors.dateHired = "Date hired is required.";
  if (!form.employmentStatus) validationErrors.employmentStatus = "Employment status is required.";
  if (!form.firstName.trim()) validationErrors.firstName = "First name is required.";
  if (!form.lastName.trim()) validationErrors.lastName = "Last name is required.";
  if (!emailValue) validationErrors.personalEmail = "Personal email is required.";
  if (!form.department) validationErrors.department = "Department is required.";
  if (!form.position) validationErrors.position = "Position is required.";
  if (isCustomPosition.value && !form.customPosition.trim()) {
    validationErrors.customPosition = "Custom position is required.";
  }
  if (!form.branch) validationErrors.branch = "Branch is required.";
  if (!form.bankAccount.trim()) validationErrors.bankAccount = "Bank account details are required.";

  if (!isEditingExisting.value && existingEmployeeIds.value.includes(idValue)) {
    validationErrors.employeeId = "Employee ID already exists. Please use a globally unique value.";
  }

  if (!isEditingExisting.value && existingEmails.value.includes(emailValue)) {
    validationErrors.personalEmail = "Personal Email already exists. Please use a unique email address.";
  }

  if (!validStatutory(form.sss, /^\d{2}-\d{7}-\d{1}$/)) {
    validationErrors.sss = "SSS must follow a valid Philippine format such as 12-3456789-0.";
  }

  if (!validStatutory(form.philhealth, /^\d{2}-\d{9}-\d{1}$/)) {
    validationErrors.philhealth = "PhilHealth must follow a valid Philippine format such as 12-345678901-2.";
  }

  if (!validStatutory(form.pagibig, /^\d{4}-\d{4}-\d{4}$/)) {
    validationErrors.pagibig = "Pag-IBIG must follow a formatted pattern such as 1234-5678-9012.";
  }

  if (!validStatutory(form.tin, /^\d{3}-\d{3}-\d{3}-\d{3}$/)) {
    validationErrors.tin = "TIN must follow a formatted numeric pattern such as 123-456-789-000.";
  }

  if (showOffboardingPanel.value && (!form.offboardingDate || !form.offboardingReason)) {
    if (!form.offboardingDate) validationErrors.offboardingDate = "Offboarding date is required.";
    if (!form.offboardingReason) validationErrors.offboardingReason = "Offboarding reason is required.";
  }

  if (Object.keys(validationErrors).length) {
    setAlert("danger", "Please complete the highlighted required fields. Optional blank fields can be skipped.");
    return false;
  }

  setAlert("success", `${fullName} is ready to be saved as a new employee profile.`);
  return true;
}

function saveDraft() {
  profileState.value = "Draft";
  setAlert("primary", "Employee profile draft saved locally.");
}

function startNewEmployee() {
  clearValidationErrors();
  Object.assign(form, createEmptyForm());
  loadedEmployeeId.value = "";
  isEditingExisting.value = false;
  profileState.value = "Draft";
  ensureGeneratedEmployeeId();
  setAlert("primary", `${form.employeeId} is ready for a new employee profile.`);
}

function loadEmployeeRecord(idValue) {
  const record = employeeRecords[idValue];
  if (!record) return;

  clearValidationErrors();
  Object.assign(form, createEmptyForm(), record, {
    employeeId: idValue,
    documents: {
      contract: true,
      govIds: true,
      bankForm: true,
      clearance: record.accountStatus === "Separated",
    },
  });
  syncPositionSelection();

  loadedEmployeeId.value = idValue;
  isEditingExisting.value = true;
  profileState.value = "Loaded";
  setAlert("info", `${idValue} loaded into the employee profile form.`);
}

function buildEmployeePayload() {
  return {
    employee_code: form.employeeId.trim(),
    first_name: form.firstName.trim(),
    middle_name: form.middleName.trim() || null,
    last_name: form.lastName.trim(),
    email: form.personalEmail.trim().toLowerCase(),
    contact_number: form.contactNumber.trim() || null,
    birth_date: form.birthDate || null,
    address: form.address.trim() || null,
    date_hired: form.dateHired || null,
    department: form.department,
    position: effectivePosition.value,
    branch: form.branch || null,
    manager: form.manager || null,
    employment_status: form.employmentStatus,
    account_status: form.accountStatus || null,
    onboarding_stage: form.onboardingStage || null,
    movement_type: form.movementType || null,
    movement_effective_date: form.movementEffectiveDate || null,
    movement_remarks: form.movementRemarks.trim() || null,
    offboarding_date: form.offboardingDate || null,
    offboarding_reason: form.offboardingReason || null,
    sss: form.sss.trim() || null,
    philhealth: form.philhealth.trim() || null,
    pagibig: form.pagibig.trim() || null,
    tin: form.tin.trim() || null,
    bank_account: form.bankAccount.trim() || null,
    emergency_contact: form.emergencyContact.trim() || null,
    notes: form.notes.trim() || null,
  };
}

function syncFormWithEmployee(employee) {
  employeeRecords[employee.employee_code] = buildEmployeeRecord(employee);
  loadEmployeeRecord(employee.employee_code);
}

async function handleSubmit() {
  ensureGeneratedEmployeeId();
  ensureUniqueGeneratedEmployeeId();

  if (!validateForm()) {
    return;
  }

  const summary = [
    `Name: ${[form.firstName, form.middleName, form.lastName].filter(Boolean).join(" ")}`,
    `Assignment: ${form.department} / ${effectivePosition.value} / ${form.branch}`,
    `Status: ${form.employmentStatus}`,
    `Onboarding: ${form.onboardingStage}`,
    `Movement: ${form.movementType}${form.movementEffectiveDate ? ` (${form.movementEffectiveDate})` : ""}`,
  ];

  form.notes = summary.join(" | ");
  if (form.offboardingReason) {
    form.notes += ` | Offboarding: ${form.offboardingReason}${form.offboardingDate ? ` (${form.offboardingDate})` : ""}`;
  }

  isSubmitting.value = true;

  try {
    const wasEditing = isEditingExisting.value;
    const payload = buildEmployeePayload();
    const employee = isEditingExisting.value
      ? await apiRequest(`/employees/${encodeURIComponent(form.employeeId.trim())}`, {
          method: "PUT",
          token: authStore.accessToken,
          body: JSON.stringify({
            ...payload,
            employee_code: undefined,
          }),
        })
      : await apiRequest("/employees", {
          method: "POST",
          token: authStore.accessToken,
          body: JSON.stringify(payload),
        });

    upsertDirectoryEntry();
    syncFormWithEmployee(employee);
    profileState.value = "Saved";
    setAlert(
      "success",
      wasEditing
        ? `${form.employeeId.trim()} updated successfully in the HRIS API.`
        : `${form.employeeId.trim()} created successfully in the HRIS API.`
    );
  } catch (error) {
    if (error instanceof ApiError && error.status === 409) {
      setAlert("danger", error.message);
    } else if (error instanceof ApiError && error.status === 401) {
      setAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
    } else {
      setAlert("danger", "Could not save to the HRIS API. Please make sure the FastAPI backend is running.");
    }
  } finally {
    isSubmitting.value = false;
  }
}

function normalizeEmployeeRow(employee) {
  const isRegular = employee.employment_status === "Regular";
  const lifecycle = isRegular ? "completed" : "onboarding";

  return {
    id: employee.employee_code,
    name: `${employee.first_name} ${employee.last_name}`,
    assignment: `${employee.department} / ${employee.position} / ${employee.branch || "Main Branch"}`,
    account: (employee.account_status || (isRegular ? "Active" : employee.employment_status)).toLowerCase(),
    employment: employee.employment_status.toLowerCase(),
    lifecycle: employee.offboarding_reason ? "offboarding" : lifecycle,
    documents: 3,
    email: employee.email,
    statusLabel: employee.account_status || (isRegular ? "Active" : employee.employment_status),
    statusClass:
      (employee.account_status || (isRegular ? "Active" : employee.employment_status)) === "Active"
        ? "bg-light-success text-success"
        : (employee.account_status || "") === "Separated"
          ? "bg-light-danger text-danger"
          : "bg-light-warning text-warning",
    lifecycleLabel: employee.offboarding_reason ? "Offboarding" : lifecycle === "completed" ? "Completed" : "Onboarding",
    lifecycleClass: employee.offboarding_reason
      ? "bg-light-danger text-danger"
      : lifecycle === "completed"
        ? "bg-light-info text-info"
        : "bg-light-warning text-warning",
  };
}

function buildEmployeeRecord(employee) {
  const departmentPositions = positionOptionsByDepartment[employee.department] || [];
  const hasKnownPosition = departmentPositions.includes(employee.position);

  return {
    firstName: employee.first_name,
    middleName: employee.middle_name || "",
    lastName: employee.last_name,
    personalEmail: employee.email,
    dateHired: employee.date_hired || "",
    employmentStatus: employee.employment_status,
    accountStatus: employee.account_status || (employee.employment_status === "Regular" ? "Active" : "Inactive"),
    contactNumber: employee.contact_number || "",
    birthDate: employee.birth_date || "",
    address: employee.address || "",
    department: employee.department,
    position: hasKnownPosition ? employee.position : "__custom",
    customPosition: hasKnownPosition ? "" : employee.position,
    branch: employee.branch || "Main Branch",
    manager: employee.manager || "",
    onboardingStage: employee.onboarding_stage || (employee.employment_status === "Regular" ? "Completed" : "Onboarding"),
    movementType: employee.movement_type || "None",
    movementEffectiveDate: employee.movement_effective_date || "",
    movementRemarks: employee.movement_remarks || "",
    offboardingDate: employee.offboarding_date || "",
    offboardingReason: employee.offboarding_reason || "",
    sss: employee.sss || "",
    philhealth: employee.philhealth || "",
    pagibig: employee.pagibig || "",
    tin: employee.tin || "",
    bankAccount: employee.bank_account || "",
    emergencyContact: employee.emergency_contact || "",
    notes: employee.notes || "",
  };
}

async function fetchEmployees() {
  if (!authStore.accessToken) {
    directoryError.value = "Sign in first to load employee records.";
    return;
  }

  isDirectoryLoading.value = true;
  directoryError.value = "";

  try {
    const response = await apiRequest("/employees", {
      token: authStore.accessToken,
    });

    const apiRows = response.items.map((employee) => {
      employeeRecords[employee.employee_code] = buildEmployeeRecord(employee);
      return normalizeEmployeeRow(employee);
    });

    baseDirectory.value = apiRows;
    ensureGeneratedEmployeeId();
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      directoryError.value = "Your session expired. Please sign in again.";
      authStore.logout();
    } else {
      directoryError.value = "Could not reach the HRIS API. No local employee records are shown.";
      baseDirectory.value = [];
      ensureGeneratedEmployeeId();
    }
  } finally {
    isDirectoryLoading.value = false;
  }
}

function upsertDirectoryEntry() {
  const entry = {
    id: form.employeeId.trim(),
    name: [form.firstName.trim(), form.lastName.trim()].filter(Boolean).join(" "),
    assignment: `${form.department || "-"} / ${effectivePosition.value || "-"} / ${form.branch || "-"}`,
    account: form.accountStatus === "Active" ? "active" : form.accountStatus.toLowerCase(),
    employment: (form.employmentStatus || "unknown").toLowerCase(),
    lifecycle: showOffboardingPanel.value ? "offboarding" : (form.onboardingStage || "pre-boarding").toLowerCase(),
    documents: documentCount.value,
    email: form.personalEmail.trim().toLowerCase(),
    statusLabel: form.accountStatus,
    statusClass:
      form.accountStatus === "Active"
        ? "bg-light-success text-success"
        : form.accountStatus === "Inactive"
          ? "bg-light-secondary text-secondary"
          : "bg-light-danger text-danger",
    lifecycleLabel: showOffboardingPanel.value ? "Offboarding" : form.onboardingStage,
    lifecycleClass: showOffboardingPanel.value ? "bg-light-danger text-danger" : "bg-light-info text-info",
  };

  employeeRecords[entry.id] = {
    ...createEmptyForm(),
    ...JSON.parse(JSON.stringify(form)),
  };

  const existingIndex = baseDirectory.value.findIndex((row) => row.id === entry.id);
  if (existingIndex >= 0) {
    baseDirectory.value.splice(existingIndex, 1, entry);
  } else {
    baseDirectory.value.unshift(entry);
  }

  loadedEmployeeId.value = entry.id;
  isEditingExisting.value = true;
}

watch(
  () => showOffboardingPanel.value,
  (visible) => {
    if (!visible) {
      clearFieldError("offboardingDate");
      clearFieldError("offboardingReason");
      form.offboardingDate = "";
      form.offboardingReason = "";
    }
  }
);

onMounted(() => {
  fetchEmployees();
});
</script>
