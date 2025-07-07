// StableAgents Desktop App Generator - Frontend JavaScript
class DesktopAppGenerator {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.currentApp = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadRecentProjects();
        this.checkApiHealth();
    }

    bindEvents() {
        // Main form submission
        document.getElementById('appGeneratorForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateApp();
        });

        // Navigation buttons
        document.getElementById('apiKeyBtn').addEventListener('click', () => this.showApiKeyModal());
        document.getElementById('healthBtn').addEventListener('click', () => this.checkApiHealth());
        document.getElementById('codeGenBtn').addEventListener('click', () => this.showCodeGenModal());
        document.getElementById('projectsBtn').addEventListener('click', () => this.showProjectsModal());
        document.getElementById('frameworksBtn').addEventListener('click', () => this.showFrameworksInfo());

        // Modal close buttons
        document.getElementById('closeApiKeyModal').addEventListener('click', () => this.hideModal('apiKeyModal'));
        document.getElementById('closeCodeGenModal').addEventListener('click', () => this.hideModal('codeGenModal'));
        document.getElementById('closeProjectsModal').addEventListener('click', () => this.hideModal('projectsModal'));

        // API key form
        document.getElementById('apiKeyForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.setApiKey();
        });

        // Code generation form
        document.getElementById('codeGenForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateCode();
        });

        // Success state buttons
        document.getElementById('runAppBtn').addEventListener('click', () => this.runApp());
        document.getElementById('viewCodeBtn').addEventListener('click', () => this.viewCode());
        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadApp());

        // Error state retry button
        document.getElementById('retryBtn').addEventListener('click', () => this.generateApp());

        // Copy code button
        document.getElementById('copyCodeBtn').addEventListener('click', () => this.copyCode());

        // Modal backdrop clicks
        document.querySelectorAll('[id$="Modal"]').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal(modal.id);
                }
            });
        });
    }

    async generateApp() {
        const form = document.getElementById('appGeneratorForm');
        const formData = new FormData(form);
        
        const appData = {
            description: formData.get('description'),
            app_name: formData.get('appName') || null,
            ui_framework: formData.get('uiFramework')
        };

        this.showLoadingState();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/desktop/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(appData)
            });

            const result = await response.json();

            if (result.success) {
                this.currentApp = result.app;
                this.showSuccessState(result.app);
                this.loadRecentProjects(); // Refresh projects list
            } else {
                throw new Error(result.detail || 'Failed to generate app');
            }
        } catch (error) {
            console.error('Error generating app:', error);
            this.showErrorState(error.message);
        }
    }

    async generateCode() {
        const form = document.getElementById('codeGenForm');
        const formData = new FormData(form);
        
        const codeData = {
            prompt: formData.get('codePrompt'),
            framework: formData.get('codeFramework')
        };

        try {
            const response = await fetch(`${this.apiBaseUrl}/desktop/generate-code`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(codeData)
            });

            const result = await response.json();

            if (result.success) {
                document.getElementById('codeOutput').textContent = result.code;
                document.getElementById('generatedCode').classList.remove('hidden');
            } else {
                throw new Error(result.detail || 'Failed to generate code');
            }
        } catch (error) {
            console.error('Error generating code:', error);
            alert(`Error generating code: ${error.message}`);
        }
    }

    async runApp() {
        if (!this.currentApp) return;

        try {
            const response = await fetch(`${this.apiBaseUrl}/desktop/run/${this.currentApp.name}`, {
                method: 'POST'
            });

            const result = await response.json();

            if (result.success) {
                alert('Application started successfully!');
            } else {
                alert(`Failed to start application: ${result.message}`);
            }
        } catch (error) {
            console.error('Error running app:', error);
            alert(`Error running app: ${error.message}`);
        }
    }

    async loadRecentProjects() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/desktop/projects`);
            const result = await response.json();

            if (result.success) {
                this.displayProjects(result.projects);
            }
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    }

    displayProjects(projects) {
        const container = document.getElementById('recentProjects');
        
        if (projects.length === 0) {
            container.innerHTML = `
                <div class="col-span-full text-center py-8">
                    <i class="fas fa-folder-open text-4xl text-gray-400 mb-4"></i>
                    <p class="text-gray-600">No projects generated yet</p>
                    <p class="text-sm text-gray-500">Create your first desktop app above!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = projects.slice(0, 6).map(project => `
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex items-center justify-between mb-2">
                    <h4 class="font-semibold text-gray-900">${project.metadata?.name || project.path.split('/').pop()}</h4>
                    <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">${project.metadata?.framework || 'Unknown'}</span>
                </div>
                <p class="text-sm text-gray-600 mb-3 line-clamp-2">${project.metadata?.description || 'No description available'}</p>
                <div class="flex space-x-2">
                    <button onclick="appGenerator.runProject('${project.path.split('/').pop()}')" 
                            class="text-xs bg-green-600 text-white px-2 py-1 rounded hover:bg-green-700">
                        <i class="fas fa-play mr-1"></i>Run
                    </button>
                    <button onclick="appGenerator.viewProject('${project.path}')" 
                            class="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700">
                        <i class="fas fa-eye mr-1"></i>View
                    </button>
                </div>
            </div>
        `).join('');
    }

    async runProject(projectName) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/desktop/run/${projectName}`, {
                method: 'POST'
            });

            const result = await response.json();

            if (result.success) {
                alert('Project started successfully!');
            } else {
                alert(`Failed to start project: ${result.message}`);
            }
        } catch (error) {
            console.error('Error running project:', error);
            alert(`Error running project: ${error.message}`);
        }
    }

    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const result = await response.json();

            if (result.status === 'healthy') {
                this.showNotification('API is healthy', 'success');
            } else {
                this.showNotification('API health check failed', 'error');
            }
        } catch (error) {
            console.error('API health check failed:', error);
            this.showNotification('Cannot connect to API server', 'error');
        }
    }

    async setApiKey() {
        const apiKey = document.getElementById('apiKeyInput').value;
        
        if (!apiKey) {
            alert('Please enter an API key');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/providers/set`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    provider: 'gemini',
                    api_key: apiKey
                })
            });

            const result = await response.json();

            if (result.success) {
                this.hideModal('apiKeyModal');
                this.showNotification('API key set successfully', 'success');
                document.getElementById('apiKeyInput').value = '';
            } else {
                throw new Error(result.detail || 'Failed to set API key');
            }
        } catch (error) {
            console.error('Error setting API key:', error);
            alert(`Error setting API key: ${error.message}`);
        }
    }

    showLoadingState() {
        document.getElementById('defaultState').classList.add('hidden');
        document.getElementById('successState').classList.add('hidden');
        document.getElementById('errorState').classList.add('hidden');
        document.getElementById('loadingState').classList.remove('hidden');
    }

    showSuccessState(app) {
        document.getElementById('defaultState').classList.add('hidden');
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('errorState').classList.add('hidden');
        document.getElementById('successState').classList.remove('hidden');

        const appDetails = document.getElementById('appDetails');
        appDetails.innerHTML = `
            <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                    <span class="font-semibold text-gray-700">Name:</span>
                    <span class="text-gray-900">${app.name}</span>
                </div>
                <div>
                    <span class="font-semibold text-gray-700">Framework:</span>
                    <span class="text-gray-900">${app.framework}</span>
                </div>
                <div class="col-span-2">
                    <span class="font-semibold text-gray-700">Location:</span>
                    <span class="text-gray-900">${app.project_path}</span>
                </div>
            </div>
        `;
    }

    showErrorState(message) {
        document.getElementById('defaultState').classList.add('hidden');
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('successState').classList.add('hidden');
        document.getElementById('errorState').classList.remove('hidden');

        document.getElementById('errorMessage').textContent = message;
    }

    showApiKeyModal() {
        document.getElementById('apiKeyModal').classList.remove('hidden');
    }

    showCodeGenModal() {
        document.getElementById('codeGenModal').classList.remove('hidden');
        document.getElementById('generatedCode').classList.add('hidden');
    }

    async showProjectsModal() {
        document.getElementById('projectsModal').classList.remove('hidden');
        await this.loadProjectsList();
    }

    async loadProjectsList() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/desktop/projects`);
            const result = await response.json();

            const projectsList = document.getElementById('projectsList');
            
            if (result.success && result.projects.length > 0) {
                projectsList.innerHTML = result.projects.map(project => `
                    <div class="border border-gray-200 rounded-lg p-4">
                        <div class="flex items-center justify-between mb-2">
                            <h4 class="font-semibold text-gray-900">${project.metadata?.name || project.path.split('/').pop()}</h4>
                            <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">${project.metadata?.framework || 'Unknown'}</span>
                        </div>
                        <p class="text-sm text-gray-600 mb-3">${project.metadata?.description || 'No description available'}</p>
                        <div class="flex space-x-2">
                            <button onclick="appGenerator.runProject('${project.path.split('/').pop()}')" 
                                    class="text-sm bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">
                                <i class="fas fa-play mr-1"></i>Run
                            </button>
                            <button onclick="appGenerator.viewProject('${project.path}')" 
                                    class="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">
                                <i class="fas fa-eye mr-1"></i>View
                            </button>
                        </div>
                    </div>
                `).join('');
            } else {
                projectsList.innerHTML = `
                    <div class="text-center py-8">
                        <i class="fas fa-folder-open text-4xl text-gray-400 mb-4"></i>
                        <p class="text-gray-600">No projects found</p>
                        <p class="text-sm text-gray-500">Create your first desktop app to get started!</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading projects list:', error);
            document.getElementById('projectsList').innerHTML = `
                <div class="text-center py-8">
                    <i class="fas fa-exclamation-triangle text-4xl text-red-400 mb-4"></i>
                    <p class="text-red-600">Error loading projects</p>
                    <p class="text-sm text-gray-500">${error.message}</p>
                </div>
            `;
        }
    }

    async showFrameworksInfo() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/desktop/frameworks`);
            const result = await response.json();

            if (result.success) {
                const frameworks = result.frameworks;
                const info = frameworks.map(fw => `${fw.name}: ${fw.description}`).join('\n');
                alert(`Supported Frameworks:\n\n${info}`);
            } else {
                throw new Error(result.detail || 'Failed to load frameworks');
            }
        } catch (error) {
            console.error('Error loading frameworks:', error);
            alert(`Error loading frameworks: ${error.message}`);
        }
    }

    hideModal(modalId) {
        document.getElementById(modalId).classList.add('hidden');
    }

    viewCode() {
        if (!this.currentApp) return;
        
        // For now, just show an alert with the project path
        alert(`App code is located at: ${this.currentApp.project_path}\n\nOpen the project folder to view the generated code.`);
    }

    downloadApp() {
        if (!this.currentApp) return;
        
        // For now, just show an alert with the project path
        alert(`App is located at: ${this.currentApp.project_path}\n\nYou can copy this folder to download your application.`);
    }

    copyCode() {
        const codeOutput = document.getElementById('codeOutput');
        const text = codeOutput.textContent;
        
        navigator.clipboard.writeText(text).then(() => {
            this.showNotification('Code copied to clipboard!', 'success');
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showNotification('Code copied to clipboard!', 'success');
        });
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg text-white z-50 transform transition-all duration-300 translate-x-full`;
        
        if (type === 'success') {
            notification.className += ' bg-green-600';
        } else if (type === 'error') {
            notification.className += ' bg-red-600';
        } else {
            notification.className += ' bg-blue-600';
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.appGenerator = new DesktopAppGenerator();
}); 