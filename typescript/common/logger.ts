export enum loggingLevel {
    DEBUG = 10,
    INFO = 20,
    WARNING = 30,
    ERROR = 40,
    CRITICAL = 50,
}

const loggingLevelNumberToString = {
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL"
}

class Logger {
    private level: loggingLevel;
    private includeTimestamp: boolean;

    constructor (level: loggingLevel = loggingLevel.DEBUG, includeTimestamp: boolean = true) {
        this.level = level;
        this.includeTimestamp = includeTimestamp;
    };

    public setLevel(level: number) {
        this.level = level;
    }

    public log(level: loggingLevel, message: string) {
        if (level < this.level) {
            return;
        }

        let logMessage = this.formatLogMessage(level, message);
        console.log(logMessage);
    }
    
    public debug(message: string) {
        this.log(loggingLevel.DEBUG, message);
    }

    public info(message: string) {
        this.log(loggingLevel.INFO, message);
    }

    public warning(message: string) {
        this.log(loggingLevel.WARNING, message);
    }

    public error(message: string) {
        this.log(loggingLevel.ERROR, message);
    }

    public critical(message: string) {
        this.log(loggingLevel.CRITICAL, message);
    }

    private formatLogMessage(level: loggingLevel, message: string): string {
        let logMessage = "";

        if (this.includeTimestamp) {
            logMessage += `${this.getCurrentDatetime()} : `;
        }

        logMessage += `${loggingLevelNumberToString[level]} : `;
        logMessage += message;
        return logMessage;
    }

    private getCurrentDatetime(): string {
        const date = new Date();
        const [datetime, milliseconds] =  date.toISOString().split('.');
        return datetime;
    }

}

const logger = new Logger();
export default logger;
