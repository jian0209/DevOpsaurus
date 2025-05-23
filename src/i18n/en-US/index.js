export default {
  loginPage: {
    username: "Username",
    password: "Password",
    loginBtn: "Login",
    mfaCode: "MFA Code",
    newPassword: "New Password",
    oldPassword: "Old Password",
    submitBtn: "Submit",
  },
  upsPage: {
    title: "UPS Page",
    subtitle: "Monitor UPS Status (Click on Row to View Details)",
    viewDialog: {
      title: "UPS Information Details",
    },
  },
  nodesPage: {
    monitor: {
      title: "Monitor Nodes Page",
      subtitle: "View Nodes Status",
    },
  },
  databasePage: {
    view: {
      title: "View Database Data Page",
      subtitle:
        "Select Database and Table to View Data (Click on Row to View Details)",
      dialog: {
        title: "Database Data Details",
      },
    },
  },
  commandPage: {
    title: "Command Page",
    subtitle: "Execute Command (Click on Row to View Details)",
    executeDialog: {
      title: "Command Information Details",
    },
  },
  logsPage: {
    userLogin: {
      title: "User Login Logs Page",
      subtitle:
        "View User Logged In (Save Only half year logs) (Click on Row to View Details)",
      infoDialog: {
        title: "User Login Information Details",
      },
    },
    system: {
      title: "System Logs Page",
      subtitle:
        "View System Logs (Save Only half year logs) (Click on Row to View Details)",
      infoDialog: {
        title: "System Logs Information Details",
      },
    },
  },
  settingsPage: {
    database: {
      title: "Database Settings Page",
      subtitle: "Configure Database Connection (Currently only support MySQL)",
      test: "Get Databases and Tables",
      parameterPlaceholder: "id IN {ids} AND / OR name = {name}",
      parameterHint: "* Eg: id IN {variable1} AND name IN {variable2}",
    },
    button: {
      add: "Add {name}",
    },
    dialog: {
      edit: {
        title: "Edit {name}",
      },
      enable: {
        title: "Enable {name}",
        subtitle: "This will Enable {name} <{target}> Be View or Edit By User",
      },
      disable: {
        title: "Disable {name}",
        subtitle: "This will Disable {name} <{target}> Be View or Edit By User",
      },
      remove: {
        title: "Remove {name}",
        subtitle: "This will Remove {name} <{target}> From Database",
      },
      info: {
        title: "{name} Information Details",
      },
    },
  },
  dialog: {
    welcome: "Welcome {name}!!!",
    logout: "Logout Successfully",
    executeSuccess: "Command {command} executed successfully.",
  },
  notify: {
    mfaEmpty: "MFA code is required.",
    passwordEmpty: "Password is required.",
    getQrCodeFailed: "Get QR code failed.",
    changePasswordSuccess: "Change password successfully.",
    sessionExpired: "Session expired, please login again.",
    configurationSaved: "Configuration saved successfully.",
    testSent: "Test {platform} sent successfully.",
    testSuccess: "Test Connection success.",
  },
  loading: {
    logout: "Logging out...",
  },
  table: {
    column: {
      action: "Action",
      auth: "Auth",
      command: "Command",
      createdAt: "Created At",
      database: "Database",
      description: "Description",
      get: "Get",
      getUrl: "Get URL",
      group: "Group",
      groupName: "Group Name",
      groupUrl: "Group URL",
      host: "Host",
      id: "ID",
      ipAddr: "IP Address",
      lastLoginIp: "Last Login IP",
      lastLoginTime: "Last Login Time",
      location: "Location",
      mfaStatus: "MFA Status",
      name: "Name",
      parameter: "Parameter",
      port: "Port",
      reason: "Reason",
      role: "Role",
      source: "Source",
      sshPort: "SSH Port",
      status: "Status",
      table: "Table",
      target: "Target",
      targetUrl: "Target URL",
      timeFetch: "Time Fetch",
      userAgent: "User Agent",
      userId: "User ID",
      username: "Username",
    },
    row: {
      enabled: "Enabled",
      disabled: "Disabled",
      success: "Success",
      failed: "Failed",
      operate: {
        info: "Info",
        edit: "Edit",
        remove: "Remove",
        enable: "Enable",
        disable: "Disable",
        refresh: "Refresh",
      },
    },
  },
  api: {
    0: "Success",
    1001: "Invalid parameter",
    1002: "Existed ip",
    1003: "Invalid ip",
    1004: "Currently is in production env",
    1005: "Currently is in pre env",
    1006: "User not found",
    1007: "User existed",
    1008: "Invalid username or password",
    1009: "Find your account is disabled, please contact admin to enable it.",
    1010: "Admin token not found",
    1011: "Your MFA is disabled, please contact admin to enable it.",
    1012: "Your MFA is not set, please set it now.",
    1013: "Invalid MFA code",
    1014: "MFA too many attempts, please try again 30 minutes later.",
    1015: "Invalid old password",
    1016: "Command name existed",
    1017: "Command not found",
    1018: "SSH authentication error",
    1019: "SSH connection error",
    1020: "SSH exception",
    1021: "Database name existed",
    1022: "Database not found",
    1023: "Database connection failed",
    1024: "Nodes existed",
    1025: "Nodes not found",
    1026: "Redis existed",
    1027: "Redis not found",
    1028: "Redis connection failed",

    9001: "System internal exception",
    9002: "Page not found",
    9003: "Unsupported media type",
    9004: "403 Forbidden",
    9005: "400 Bad request",

    9999: "Network Error",

    unknown: "Check backend service logs for more details.",
  },
  underConstruction: "UNDER CONSTRUCTION!!!",
};
