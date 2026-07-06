<template>
  <!-- Reuse the exact same fill-up form UI as EmployeeProfilePage.vue, but in NEW mode -->
  <div>
    <BreadcrumbBar section="HR Modules / Employee Master" current="New Employee" />

    <div class="row g-3">
      <div class="col-lg-8 order-2 order-lg-1">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-3">
              <button
                class="btn btn-sm btn-outline-secondary d-flex align-items-center justify-content-center"
                style="width: 32px; height: 32px; padding: 0;"
                @click="goBack"
                title="Back to Directory"
              >
                <i class="ti ti-arrow-left"></i>
              </button>
              <div>
                <h5 class="mb-0">New Employee</h5>
                <small class="text-muted">Fill out the form to create a new employee record.</small>
              </div>
            </div>
            <span class="badge bg-light-primary text-primary">Draft</span>
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
                  <input id="employeeId" v-model="form.employeeId" type="text" class="form-control" placeholder="EMP-0001" readonly>
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
                  <input id="middleName" v-model="form.middleName" type="text" class="form-control" @input="handleFormMutation('middleName')">
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
                  <input id="contactNumber" v-model="form.contactNumber" type="text" class="form-control" placeholder="0917-123-4567" @input="handleFormMutation('contactNumber')">
                </div>

                <div class="col-md-3 mb-3">
                  <label class="form-label" for="birthDate">Birth Date</label>
                  <input id="birthDate" v-model="form.birthDate" type="date" class="form-control" @input="handleFormMutation('birthDate')">
                </div>

                <div class="col-md-8 mb-3">
                  <label class="form-label" for="address">Address</label>
                  <input id="address" v-model="form.address" type="text" class="form-control" placeholder="City, province, and street address" @input="handleFormMutation('address')">
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="accountStatus">Account Status</label>
                  <select id="accountStatus" v-model="form.accountStatus" class="form-select" @change="handleFormMutation('accountStatus')">
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
                  <input id="manager" v-model="form.manager" type="text" class="form-control" placeholder="(Optional) Supervisor name" @input="handleFormMutation('manager')">
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
                  <select id="onboardingStage" v-model="form.onboardingStage" class="form-select" @change="handleFormMutation('onboardingStage')">
                    <option>Pre-boarding</option>
                    <option>Onboarding</option>
                    <option>Completed</option>
                  </select>
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="movementType">Movement Type</label>
                  <select id="movementType" v-model="form.movementType" class="form-select" @change="handleFormMutation('movementType')">
                    <option>None</option>
                    <option>Promotion</option>
                    <option>Transfer</option>
                    <option>Resignation</option>
                  </select>
                </div>

                <div class="col-md-4 mb-3">
                  <label class="form-label" for="movementEffectiveDate">Movement Effective Date</label>
                  <input id="movementEffectiveDate" v-model="form.movementEffectiveDate" type="date" class="form-control" @input="handleFormMutation('movementEffectiveDate')">
                </div>

                <div class="col-md-12 mb-3">
                  <label class="form-label" for="movementRemarks">Movement Remarks</label>
                  <input id="movementRemarks" v-model="form.movementRemarks" type="text" class="form-control" placeholder="Promotion, transfer, or resignation note" @input="handleFormMutation('movementRemarks')">
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
                  <input id="emergencyContact" v-model="form.emergencyContact" type="text" class="form-control" placeholder="Name and contact number" @input="handleFormMutation('emergencyContact')">
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label d-block">Document Checklist</label>
                  <div class="form-check mb-2">
                    <input id="docContract" v-model="form.documents.contract" class="form-check-input" type="checkbox" @change="handleFormMutation('documents')">
                    <label class="form-check-label" for="docContract">Employment Contract</label>
                  </div>
                  <div class="form-check mb-2">
                    <input id="docGovIds" v-model="form.documents.govIds" class="form-check-input" type="checkbox" @change="handleFormMutation('documents')">
                    <label class="form-check-label" for="docGovIds">Government IDs</label>
                  </div>
                  <div class="form-check mb-2">
                    <input id="docBankForm" v-model="form.documents.bankForm" class="form-check-input" type="checkbox" @change="handleFormMutation('documents')">
                    <label class="form-check-label" for="docBankForm">Bank Enrollment Form</label>
                  </div>
                  <div class="form-check">
                    <input id="docClearance" v-model="form.documents.clearance" class="form-check-input" type="checkbox" @change="handleFormMutation('documents')">
                    <label class="form-check-label" for="docClearance">Clearance / Exit Documents</label>
                  </div>
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label" for="documentUpload">Document Management</label>
                  <input id="documentUpload" type="file" class="form-control" multiple @change="handleDocumentUpload">
                  <small class="text-muted">Upload contracts, IDs, forms, or clearance files.</small>
                  <ul v-if="form.uploads.length" class="list-unstyled mt-2 mb-0">
                    <li v-for="(file, index) in form.uploads" :key="index" class="d-flex align-items-center justify-content-between border rounded px-2 py-1 mb-1">
                      <span class="small text-truncate">{{ file.name }}</span>
                      <button type="button" class="btn btn-sm btn-link text-danger p-0 ms-2" @click="removeUpload(index)">Remove</button>
                    </li>
                  </ul>
                </div>

                <div class="col-md-12 mb-3">
                  <label class="form-label" for="notes">Notes</label>
                  <input id="notes" v-model="form.notes" type="text" class="form-control" placeholder="Optional audit or HR notes" @input="handleFormMutation('notes')">
                </div>
              </div>

              <div class="d-flex flex-wrap gap-2 mt-2">
                <button type="button" class="btn btn-outline-primary" @click="saveDraft">Save Draft</button>
                <button type="submit" class="btn btn-primary" :disabled="isSubmitting">Create Employee Profile</button>
              </div>

              <div class="alert mt-3 mb-0" :class="alertState.class" role="alert">
                {{ alertState.message }}
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-4 order-1 order-lg-2 mb-3 mb-lg-0">
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
              <small class="text-muted d-block">Changing account status updates whether the employee should have active HRIS access.</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import { apiRequest, ApiError } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const departmentOptions = ["Human Resources", "Finance", "Operations", "IT"];
const positionOptionsByDepartment = {
  "Human Resources": ["HR Assistant", "HR Officer", "HR Manager", "Recruitment Specialist", "Training Coordinator"],
  Finance: ["Accounting Staff", "Bookkeeper", "Finance Analyst", "Payroll Admin", "Finance Manager"],
  Operations: ["Operations Staff", "Operations Coordinator", "Operations Supervisor", "Branch Manager", "Attendance Clerk"],
  IT: ["IT Staff", "IT Support Specialist", "System Administrator", "Network Administrator", "IT Manager"],
};

function createEmptyForm() {
  return {
    employeeId: "EMP-0001",
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

const form = reactive(createEmptyForm());
const validationErrors = reactive({});
const isSubmitting = ref(false);

const alertState = reactive({
  class: "alert-light-primary border-primary",
  message: "Fill out the profile to create a new employee record.",
});

function goBack() {
  router.push("/employees");
}

function setAlert(type, message) {
  alertState.class = `alert-light-${type} border-${type}`;
  alertState.message = message;
}

function fieldClass(fieldName) {
  return validationErrors[fieldName] ? "is-invalid" : "";
}

function clearValidationErrors() {
  Object.keys(validationErrors).forEach((k) => delete validationErrors[k]);
}

function handleFormMutation(fieldName = "") {
  if (fieldName && validationErrors[fieldName]) delete validationErrors[fieldName];
}

const selectedPositionOptions = computed(() => positionOptionsByDepartment[form.department] || []);
const isCustomPosition = computed(() => form.position === "__custom");

const effectivePosition = computed(() => (isCustomPosition.value ? form.customPosition.trim() : form.position));

const employeeSummary = computed(() => {
  const name = [form.firstName.trim(), form.middleName.trim(), form.lastName.trim()].filter(Boolean).join(" ");
  return name || "No employee profile yet";
});

const assignmentSummary = computed(() =>
  form.department && effectivePosition.value && form.branch
    ? `${form.department} / ${effectivePosition.value} / ${form.branch}`
    : "Department / Position / Branch"
);

const managerSummary = computed(() => form.manager || "Not assigned");
const onboardingSummary = computed(() => form.onboardingStage || "Pre-boarding");

const movementSummary = computed(() =>
  form.movementType === "None" ? "None" : form.movementEffectiveDate ? `${form.movementType} (${form.movementEffectiveDate})` : form.movementType
);

const employmentSummary = computed(() => form.employmentStatus || "-");

const documentCount = computed(() =>
  [form.documents.contract, form.documents.govIds, form.documents.bankForm, form.documents.clearance].filter(Boolean).length
);
const documentSummary = computed(() => `${documentCount.value} / 4`);

const accessPreview = computed(() => {
  if (form.accountStatus === "Active") return { label: "Active", class: "bg-light-success text-success" };
  if (form.accountStatus === "Inactive") return { label: "Restricted", class: "bg-light-warning text-warning" };
  return { label: "Removed", class: "bg-light-danger text-danger" };
});

const showOffboardingPanel = computed(
  () => form.accountStatus === "Separated" || form.movementType === "Resignation"
);

function validStatutory(value, pattern) {
  if (!value) return true;
  return pattern.test(value.trim());
}

function handleDepartmentChange() {
  validationErrors.department = undefined;
  form.position = "";
  form.customPosition = "";
  handleFormMutation();
}

function handlePositionChange() {
  if (!isCustomPosition.value) form.customPosition = "";
  handleFormMutation();
}

function handleDocumentUpload(event) {
  form.uploads = Array.from(event.target.files || []);
  handleFormMutation("uploads");
}

function removeUpload(index) {
  form.uploads.splice(index, 1);
  handleFormMutation("uploads");
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

function validateForm() {
  clearValidationErrors();

  if (!form.employeeId.trim()) validationErrors.employeeId = "Employee ID is required.";
  if (!form.dateHired) validationErrors.dateHired = "Date hired is required.";
  if (!form.employmentStatus) validationErrors.employmentStatus = "Employment status is required.";
  if (!form.firstName.trim()) validationErrors.firstName = "First name is required.";
  if (!form.lastName.trim()) validationErrors.lastName = "Last name is required.";
  if (!form.personalEmail.trim()) validationErrors.personalEmail = "Personal email is required.";
  if (!form.department) validationErrors.department = "Department is required.";
  if (!form.position) validationErrors.position = "Position is required.";
  if (isCustomPosition.value && !form.customPosition.trim()) validationErrors.customPosition = "Custom position is required.";
  if (!form.branch) validationErrors.branch = "Branch is required.";
  if (!form.bankAccount.trim()) validationErrors.bankAccount = "Bank account details are required.";

  if (!validStatutory(form.sss, /^\d{2}-\d{7}-\d{1}$/)) validationErrors.sss = "Invalid SSS format.";
  if (!validStatutory(form.philhealth, /^\d{2}-\d{9}-\d{1}$/)) validationErrors.philhealth = "Invalid PhilHealth format.";
  if (!validStatutory(form.pagibig, /^\d{4}-\d{4}-\d{4}$/)) validationErrors.pagibig = "Invalid Pag-IBIG format.";
  if (!validStatutory(form.tin, /^\d{3}-\d{3}-\d{3}-\d{3}$/)) validationErrors.tin = "Invalid TIN format.";

  if (showOffboardingPanel.value) {
    if (!form.offboardingDate) validationErrors.offboardingDate = "Offboarding date is required.";
    if (!form.offboardingReason) validationErrors.offboardingReason = "Offboarding reason is required.";
  }

  if (Object.keys(validationErrors).length) {
    setAlert("danger", "Please complete the highlighted required fields.");
    return false;
  }

  setAlert("success", "Employee profile is ready to be created.");
  return true;
}

function saveDraft() {
  setAlert("primary", "Employee profile draft saved locally.");
}

async function handleSubmit() {
  if (!validateForm()) return;

  isSubmitting.value = true;
  try {
    const payload = buildEmployeePayload();
    await apiRequest("/employees", {
      method: "POST",
      token: authStore.accessToken,
      body: JSON.stringify(payload),
    });

    setAlert("success", `${form.employeeId.trim()} created successfully.`);
    setTimeout(() => router.push("/employees"), 1500);
  } catch (error) {
    if (error instanceof ApiError && error.status === 409) setAlert("danger", error.message);
    else if (error instanceof ApiError && error.status === 401) {
      setAlert("danger", "Your session expired. Please sign in again.");
      authStore.logout();
    } else setAlert("danger", "Could not save to the HRIS API.");
  } finally {
    isSubmitting.value = false;
  }
}
</script>

