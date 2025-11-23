import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

def jobName = 'nomoney'
def displayName = 'NoMoney'
def jenkinsFilePath = '/usr/share/jenkins/ref/Jenkinsfile'

def jenkins = Jenkins.instance
def job = jenkins.getItem(jobName)

if (job == null) {
  def file = new File(jenkinsFilePath)
  def flowDefinition = new CpsFlowDefinition(file.text, true)

  job = jenkins.createProject(WorkflowJob.class, jobName)

  job.displayName = displayName
  job.setDefinition(flowDefinition)

  job.save()
}
