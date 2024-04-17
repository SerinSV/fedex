class Constants:
    HTTP_200_SUCCESS_STATUS_CODE = 200
    HTTP_500_ERROR_STATUS_CODE = 500

    class CommonKeys:
        KEY_USER_ID = "user_id"
        KEY_PROCESS_TEMPLATE = "process_template"
        KEY_SITE_TEMPLATE = "site_template"
        KEY_PROCESS_TEMPLT_ID = "process_templt_id"
        KEY_KEY_LIST = "key_list"
        KEY_VALUE = "value"
        KEY_SITE_TEMPLT_ID = "site_templt_id"
        KEY_TYPE = "type"
        KEY_LOOKUP = "lookup_name"
        KEY_CREATED_BY = "created_by"
        KEY_CREATED_TIME = "created_at"
        KEY_COMPLETED_AT = "completed_at"
        KEY_UPDATED_AT = "updated_by"
        KEY_LAST_UPDATED_TIME = "updated_at"
        MRP = "MRP"

    class CollectionNames:
        lookup_table = "lookup_table"
        camera_configurations = "camera_configuration"
        camera_configurations_old = "cameraConfiguration"
        janus_deployment = "janusDeployment"
        service_configurations = "serviceConfiguration"
        ai_models = "aiModels"
        vision_apps = "visionApps"
        count_tasks = "count_tasks"
        event_logs = "eventLogs"
        site_configuration = "siteConfiguration"
        panel_configuration = "panelConfiguration"
        ilens_device_collection = "ilens_devices"
        hierarchy_details_collection = "hierarchy_details"
        reset_count_logs_collection = "reset_count_logs"
        site_admin = "siteAdmin"
        app_details = "appDetails"
        template_details = "appTemplates"

    class CameraVideoNames:
        data = {
            "action": "switch",
            "label": "Recording Status",
            "type": "switch",
            "key": "cameraVideoStatus",
        }


class Secrets:
    LOCK_OUT_TIME_MINS = 30
    leeway_in_mins = 10
    unique_key = "45c37939-0f75"
    token = "8674cd1d-2578-4a62-8ab7-d3ee5f9a"
    issuer = "ilens"
    alg = "RS256"
    SECRET_FOR_SUPPORT_LENS = "WeSupport24X7UnifyTwinX#"
    ISS = "unifytwin"
    AUD = "supportlens"
    signature_key = "kliLensKLiLensKL"
    signature_key_alg = ["HS256"]


class PostgresDB:
    TABLE_CREATION_QUERY = """ """


class STATUS:
    SUCCESS = "success"
    FAILED = "failed"
    SUCCESS_CODES = [200, 201]


class ResponseMessage:
    app_add_success = "App Added Successfully"
