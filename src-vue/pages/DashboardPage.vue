<template>
  <div>
    <BreadcrumbBar section="Dashboard" current="Home" />

    <div class="row g-3">
      <div class="col-xl-8">
        <div class="card h-100 border-0 shadow-sm overflow-hidden">
          <div class="card-body p-4 d-flex flex-column justify-content-between h-100">
            <div class="row align-items-center g-4">
              <div class="col-12">
                <span class="badge bg-light-primary text-primary mb-3">HRIS Operations Center</span>
                <h3 class="mb-2">Track people, time, leave, payroll, and reports from one HR dashboard.</h3>
                <p class="text-muted mb-3">
                  This view is focused on the daily work of HR Admins: monitor employee changes, watch attendance issues, review approvals, and prepare payroll-ready data.
                </p>
                <div class="d-flex flex-wrap align-items-center gap-2 mb-4">
                  <RouterLink to="/employees" class="btn btn-primary">Open Employee Master</RouterLink>
                  <RouterLink to="/attendance" class="btn btn-outline-primary">Review Attendance</RouterLink>
                  <RouterLink to="/reports" class="btn btn-outline-secondary">Open Reports</RouterLink>
                </div>
              </div>
            </div>
            <div class="row g-3">
              <div class="col-md-4" v-for="card in heroStats" :key="card.label">
                <div class="border rounded-3 p-3 h-100 bg-light">
                  <small class="text-muted d-block mb-1">{{ card.label }}</small>
                  <strong class="d-block">{{ card.value }}</strong>
                  <span class="text-muted small">{{ card.caption }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-4">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-header d-flex align-items-center justify-content-between">
            <h5 class="mb-0">Approval Queue</h5>
            <span class="badge bg-light-warning text-warning">18 items</span>
          </div>
          <div class="card-body">
            <div v-for="item in approvals" :key="item.label" class="border rounded-3 p-3 mb-3">
              <div class="d-flex justify-content-between align-items-start mb-1">
                <h6 class="mb-0">{{ item.label }}</h6>
                <span class="badge" :class="item.badgeClass">{{ item.count }}</span>
              </div>
              <p class="text-muted mb-0 text-sm">{{ item.caption }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3" v-for="module in moduleStats" :key="module.title">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="mb-2 f-w-400 text-muted">{{ module.title }}</h6>
            <h4 class="mb-3">
              {{ module.value }}
              <span class="badge" :class="module.badgeClass"><i :class="module.icon"></i> {{ module.badge }}</span>
            </h4>
            <p class="mb-0 text-muted text-sm">{{ module.caption }}</p>
          </div>
        </div>
      </div>

      <div class="col-xl-8">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <h5 class="mb-0">Quick Actions</h5>
            <span class="text-muted text-sm">Most-used HR tasks</span>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6 col-lg-4" v-for="action in quickActions" :key="action.title">
                <RouterLink :to="action.to" class="text-decoration-none">
                  <div class="border rounded-3 p-3 h-100">
                    <div class="d-flex align-items-center justify-content-between mb-2">
                      <h6 class="mb-0 text-dark">{{ action.title }}</h6>
                      <i :class="action.icon"></i>
                    </div>
                    <p class="text-muted mb-0 text-sm">{{ action.caption }}</p>
                  </div>
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-4">
        <div class="card h-100">
          <div class="card-header">
            <h5 class="mb-0">Important Dates</h5>
          </div>
          <div class="card-body">
            <div v-for="date in importantDates" :key="date.label" class="d-flex align-items-start justify-content-between border-bottom pb-3 mb-3">
              <div>
                <h6 class="mb-1">{{ date.label }}</h6>
                <p class="text-muted mb-0 text-sm">{{ date.caption }}</p>
              </div>
              <span class="badge" :class="date.badgeClass">{{ date.when }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="card h-100">
          <div class="card-header d-flex align-items-center justify-content-between">
            <h5 class="mb-0">Recent Activity</h5>
            <RouterLink to="/reports" class="btn btn-sm btn-light-primary">View Reports</RouterLink>
          </div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-hover mb-0">
                <thead>
                  <tr>
                    <th>Activity</th>
                    <th>Employee</th>
                    <th>Module</th>
                    <th>Status</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="activity in recentActivity" :key="`${activity.activity}-${activity.time}`">
                    <td>{{ activity.activity }}</td>
                    <td>{{ activity.employee }}</td>
                    <td>{{ activity.module }}</td>
                    <td><span class="badge" :class="activity.badgeClass">{{ activity.status }}</span></td>
                    <td>{{ activity.time }}</td>
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
import { RouterLink } from "vue-router";
import BreadcrumbBar from "@/components/BreadcrumbBar.vue";

const heroStats = [
  { label: "Workforce", value: "0 active employee records", caption: "Add employees from Employee Master" },
  { label: "Attendance", value: "0 present today", caption: "No attendance logs yet" },
  { label: "Payroll", value: "No open cutoff", caption: "Create payroll runs from Payroll" },
];

const approvals = [
  {
    label: "Leave Requests",
    count: "0",
    caption: "No leave requests waiting for approval.",
    badgeClass: "bg-light-warning text-warning",
  },
  {
    label: "Attendance Corrections",
    count: "0",
    caption: "No attendance correction requests need supervisor review.",
    badgeClass: "bg-light-info text-info",
  },
  {
    label: "Payroll Exceptions",
    count: "0",
    caption: "No payroll exceptions are waiting for review.",
    badgeClass: "bg-light-danger text-danger",
  },
];

const moduleStats = [
  {
    title: "Employee Master",
    value: "0",
    badge: "Ready",
    badgeClass: "bg-light-primary border border-primary",
    icon: "ti ti-users",
    caption: "Profiles, status changes, onboarding, offboarding, and document tracking.",
  },
  {
    title: "Attendance Control",
    value: "0",
    badge: "No logs",
    badgeClass: "bg-light-success border border-success",
    icon: "ti ti-clock-check",
    caption: "Shift logs, late cases, undertime, overtime, and correction requests.",
  },
  {
    title: "Leave Management",
    value: "0",
    badge: "None",
    badgeClass: "bg-light-warning border border-warning",
    icon: "ti ti-calendar-event",
    caption: "Balances, leave types, approval flow, cancellations, and payroll impact.",
  },
  {
    title: "Payroll Run",
    value: "Draft",
    badge: "Cutoff open",
    badgeClass: "bg-light-danger border border-danger",
    icon: "ti ti-wallet",
    caption: "Compensation, deductions, premiums, and payslip publication are still under review.",
  },
];

const quickActions = [
  { to: "/employees", title: "Add Employee", icon: "ti ti-user-plus text-primary", caption: "Create a profile and begin onboarding." },
  { to: "/attendance", title: "Attendance Review", icon: "ti ti-clock text-info", caption: "Check late logs, OT, and correction requests." },
  { to: "/leave", title: "Leave Approval", icon: "ti ti-calendar-plus text-warning", caption: "Review leave requests and balances." },
  { to: "/payroll", title: "Run Payroll", icon: "ti ti-cash text-danger", caption: "Review cutoff, deductions, and payroll summary." },
  { to: "/accounts", title: "Add Account", icon: "ti ti-user-cog text-secondary", caption: "Create sign-in access for HRIS users." },
  { to: "/reports", title: "Generate Reports", icon: "ti ti-report-analytics text-success", caption: "Export employee, attendance, leave, and payroll data." },
];

const importantDates = [
  { label: "Payroll Cutoff End", caption: "No payroll cutoff configured yet.", when: "-", badgeClass: "bg-light-secondary text-secondary" },
];

const recentActivity = [];
</script>
